#!/usr/bin/env python3
"""Straighten photos of bookcases with a homography (see strip.sh).

A photo of a flat thing is a projective transformation of it: with the
front of a bookcase as a rectangle in the plane, every point (x, y) on
it lands in the photo at (u/w, v/w) where [u v w]^T = H [x y 1]^T and H
is a 3x3 matrix defined up to scale, so 8 unknowns. Four corners give 8
equations. Run backwards, H^-1 takes the photo to a straight-on view.

What's in here:

  homography()    the direct linear transform: stack two equations per
                  corner into an 8x9 matrix A and take its null vector
                  from the SVD (the right singular vector of the
                  smallest singular value). Points are normalized first
                  (Hartley), which keeps A well conditioned.
  aspect_ratio()  the rectangle's true width/height. The four corners
                  alone don't say how wide the case really is, since a
                  narrow case seen head on and a wide one seen at an
                  angle can look the same. With the camera's focal length,
                  they do (Zhang & He, "Whiteboard scanning and image
                  enhancement", 2007): the two vanishing directions of a
                  rectangle's sides must be perpendicular in 3D, which
                  pins down the ratio. The same constraint can instead
                  be solved for the focal length, as a cross-check
                  against EXIF.
  warp()          inverse mapping: for every output pixel, H takes it
                  back into the photo, where it's sampled bilinearly.

Corners are TL, TR, BL, BR in full-resolution pixels.
"""

import json
import sys

import numpy as np
from PIL import Image


def normalize(pts):
    """Similarity T taking pts to centroid 0, mean distance sqrt(2)."""
    c = pts.mean(axis=0)
    s = np.sqrt(2) / np.mean(np.linalg.norm(pts - c, axis=1))
    return np.array([[s, 0, -s * c[0]], [0, s, -s * c[1]], [0, 0, 1]])


def homography(src, dst):
    """H with dst ~ H src, from 4+ point pairs, by DLT."""
    src, dst = np.asarray(src, float), np.asarray(dst, float)
    Ts, Td = normalize(src), normalize(dst)
    s = (Ts @ np.c_[src, np.ones(len(src))].T).T
    d = (Td @ np.c_[dst, np.ones(len(dst))].T).T
    rows = []
    for (x, y, _), (u, v, _) in zip(s, d):
        rows.append([-x, -y, -1, 0, 0, 0, u * x, u * y, u])
        rows.append([0, 0, 0, -x, -y, -1, v * x, v * y, v])
    A = np.array(rows)
    _, sv, Vt = np.linalg.svd(A)
    H = Vt[-1].reshape(3, 3)  # the null vector: A h = 0
    H = np.linalg.inv(Td) @ H @ Ts
    return H / H[2, 2], sv


def aspect_ratio(corners, f, center):
    """True width/height of the rectangle, and the focal length the
    corners themselves imply (Zhang & He)."""
    m1, m2, m3, m4 = (np.array([x, y, 1.0]) for x, y in corners)
    k2 = np.dot(np.cross(m1, m4), m3) / np.dot(np.cross(m2, m4), m3)
    k3 = np.dot(np.cross(m1, m4), m2) / np.dot(np.cross(m3, m4), m2)
    n2 = k2 * m2 - m1
    n3 = k3 * m3 - m1
    u0, v0 = center

    # Focal length from orthogonality alone (unstable when the photo is
    # nearly head on, which is why EXIF is used for the ratio).
    num = (n2[0] * n3[0] - (n2[0] * n3[2] + n2[2] * n3[0]) * u0 + n2[2] * n3[2] * u0 * u0
           + n2[1] * n3[1] - (n2[1] * n3[2] + n2[2] * n3[1]) * v0 + n2[2] * n3[2] * v0 * v0)
    den = n2[2] * n3[2]
    f2 = -num / den if den else float("nan")
    f_implied = np.sqrt(f2) if f2 > 0 else float("nan")

    Ainv = np.linalg.inv(np.array([[f, 0, u0], [0, f, v0], [0, 0, 1.0]]))
    B = Ainv.T @ Ainv
    ratio = np.sqrt((n2 @ B @ n2) / (n3 @ B @ n3))
    return ratio, f_implied


def warp(img, Hinv, size):
    """Sample img at Hinv [x y 1] for every output pixel, bilinearly."""
    w, h = size
    xs, ys = np.meshgrid(np.arange(w) + 0.5, np.arange(h) + 0.5)
    p = Hinv @ np.stack([xs.ravel(), ys.ravel(), np.ones(xs.size)])
    u = p[0] / p[2] - 0.5
    v = p[1] / p[2] - 0.5
    x0 = np.clip(np.floor(u).astype(int), 0, img.shape[1] - 2)
    y0 = np.clip(np.floor(v).astype(int), 0, img.shape[0] - 2)
    fx = np.clip(u - x0, 0, 1)[:, None]
    fy = np.clip(v - y0, 0, 1)[:, None]
    a = img[y0, x0] * (1 - fx) + img[y0, x0 + 1] * fx
    b = img[y0 + 1, x0] * (1 - fx) + img[y0 + 1, x0 + 1] * fx
    out = a * (1 - fy) + b * fy
    return out.reshape(h, w, -1).clip(0, 255).astype(np.uint8)


def main():
    spec = json.load(open(sys.argv[1]))
    height = spec.get("height", 1800)
    margin = spec.get("margin", 0.025)  # of the height, around the case
    for case in spec["cases"]:
        img = np.asarray(Image.open(case["photo"]).convert("RGB"), float)
        H_img, W_img = img.shape[:2]
        # Pixel focal length from the 35 mm equivalent. Phones crop 16:9
        # from a 4:3 sensor keeping the long side, so the 35 mm diagonal
        # matches a 4:3 frame on that side.
        long = max(H_img, W_img)
        f = spec["focal35"] * (long * 5 / 4) / 43.27
        ratio, f_implied = aspect_ratio(case["corners"], f, (W_img / 2, H_img / 2))

        m = margin * height
        w = ratio * height
        dst = [(m, m), (m + w, m), (m, m + height), (m + w, m + height)]
        H, sv = homography(case["corners"], dst)
        out = warp(img, np.linalg.inv(H), (int(round(w + 2 * m)), int(round(height + 2 * m))))
        Image.fromarray(out).save(case["out"], quality=90)
        p = H @ np.c_[np.array(case["corners"], float), np.ones(4)].T
        err = np.abs((p[:2] / p[2]).T - dst).max()
        print(f"{case['out']}: width/height {ratio:.3f}, f {f:.0f} px "
              f"(the corners alone imply {f_implied:.0f}), corner error {err:.1e} px")


if __name__ == "__main__":
    main()
