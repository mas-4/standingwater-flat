#!/bin/sh
# The bookshelf strip on the reading orbit, from photos of the five cases.
#
# The photos aren't in the repo (they're big, and they're of my home).
# Put them in tools/shelves/photos/ under the names in corners.json, with
# each case's corners (top left, top right, bottom left, bottom right, in
# pixels) recorded there. rectify.py straightens each case to a head-on
# view of just its front; this lines them up.
set -eu
cd "$(dirname "$0")"
mkdir -p out
python3 rectify.py corners.json
for f in out/s?.jpg; do
  magick "$f" -channel RGB -contrast-stretch 0.2%x0.2% +channel -resize x1800 "${f%.jpg}-x1800.jpg"
done
magick out/s?-x1800.jpg -background '#142420' -splice 12x0 +append -chop 12x0 \
  -resize 2400x -strip -quality 80 ../../src/orbits/shelves.jpg
# And at full size, for zooming in to read the spines
for f in out/s?.jpg; do
  case "$f" in *x1800*) continue ;; esac
  magick "$f" -channel RGB -contrast-stretch 0.2%x0.2% +channel "${f%.jpg}-full.jpg"
done
magick out/s?-full.jpg -background '#142420' -splice 16x0 +append -chop 16x0 \
  -strip -quality 78 -interlace Plane ../../src/orbits/shelves-full.jpg
