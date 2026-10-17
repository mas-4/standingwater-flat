#!/usr/bin/env python3
"""A snapshot of my Anki reviews for the languages orbit.

    tools/anki.py collection.anki2     # a copy of an Anki collection
    tools/anki.py --adb                # pull one from AnkiDroid over USB

Reads the collection (read only) and rewrites the part of
src/orbits/languages.md between <!-- anki --> and <!-- /anki --> with a
heatmap of reviews per day and a table of decks by language. Only those
totals are published: no cards, and no times of day.
"""

import datetime as dt
import html
import pathlib
import sqlite3
import subprocess
import sys
import tempfile
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "src" / "orbits" / "languages.md"
ADB_PATH = "/sdcard/Android/data/com.ichi2.anki/files/AnkiDroid/collection.anki2"

# Top-level deck paths, as shown on the site. Anything else isn't listed
# (but its reviews still count in the heatmap).
GROUPS = [
    ("languages", "latin", "Latin"),
    ("languages", "greek", "Greek"),
    ("languages", "sanskrit", "Sanskrit"),
    ("languages", "chinese", "Chinese"),
    ("languages", "italian", "Italian"),
    ("languages", "spanish", "Spanish"),
    ("languages", "french", "French"),
    ("singing school", "poems", "Poems by heart"),
    ("math", None, "Math"),
]
PAUSED_AFTER = 30  # days without a review


def group_of(path):
    for top, sub, name in GROUPS:
        if path[0] == top and (sub is None or (len(path) > 1 and path[1] == sub)):
            return name
    return None


def snapshot(db):
    decks = {i: n.split("\x1f") for i, n in db.execute("select id, name from decks")}
    groups = defaultdict(lambda: {"cards": 0, "mature": 0, "reviews": 0, "last": None})
    for did, n, mature in db.execute("select did, count(*), sum(ivl >= 21) from cards group by did"):
        g = group_of(decks.get(did, ["?"]))
        if g:
            groups[g]["cards"] += n
            groups[g]["mature"] += mature
    daily = defaultdict(int)
    rows = db.execute("select r.id, c.did from revlog r left join cards c on r.cid = c.id")
    for rid, did in rows:
        day = dt.datetime.fromtimestamp(rid / 1000).date()
        daily[day] += 1
        g = group_of(decks.get(did, ["?"])) if did else None
        if g:
            groups[g]["reviews"] += 1
            groups[g]["last"] = max(groups[g]["last"] or day, day)
    return daily, groups


def streaks(daily):
    days = sorted(daily)
    longest = run = 0
    prev = None
    for d in days:
        run = run + 1 if prev and (d - prev).days == 1 else 1
        longest = max(longest, run)
        prev = d
    return longest


def heatmap(daily):
    """An SVG of weeks (columns) by weekdays (rows), GitHub style."""
    first, last = min(daily), max(daily)
    start = first - dt.timedelta(days=(first.weekday() + 1) % 7)  # a Sunday
    counts = sorted(v for v in daily.values() if v)
    # Four shades, by quartile of the days with any reviews: h1..h4
    cuts = [counts[int(len(counts) * q)] for q in (0.25, 0.5, 0.75)]
    level = lambda n: 0 if not n else 1 + sum(n > c for c in cuts)
    pitch, size, top = 9, 7.5, 14
    weeks = (last - start).days // 7 + 1
    out = [f'<svg class="heatmap" viewBox="0 0 {weeks * pitch} {top + 7 * pitch}" '
           f'role="img" aria-label="Anki reviews per day, {first:%B %Y} to {last:%B %Y}">']
    d = start
    while d <= last:
        w, r = (d - start).days // 7, (d.weekday() + 1) % 7
        if d.day == 1 and d.month in (1, 4, 7, 10):
            label = f"{d:%b %Y}" if d.month == 1 else f"{d:%b}"
            out.append(f'<text x="{w * pitch}" y="9">{label}</text>')
        if d >= first:
            n = daily.get(d, 0)
            out.append(f'<rect class="h{level(n)}" x="{w * pitch}" y="{top + r * pitch}" '
                       f'width="{size}" height="{size}"><title>{d:%b %-d, %Y}: {n} reviews</title></rect>')
        d += dt.timedelta(days=1)
    out.append("</svg>")
    return "".join(out)


def table(groups, today):
    rows = ['<table class="anki-decks">',
            "<thead><tr><th>Deck</th><th>Cards</th><th>Mature</th><th>Reviews</th><th></th></tr></thead><tbody>"]
    for _, _, name in GROUPS:
        g = groups.get(name)
        if not g or not g["reviews"]:
            continue
        idle = (today - g["last"]).days
        status = f"paused since {g['last']:%B %Y}" if idle > PAUSED_AFTER else "active"
        rows.append(f'<tr><td>{html.escape(name)}</td><td>{g["cards"]:,}</td><td>{g["mature"]:,}</td>'
                    f'<td>{g["reviews"]:,}</td><td class="status">{status}</td></tr>')
    rows.append("</tbody></table>")
    return "".join(rows)


def main():
    if sys.argv[1:] == ["--adb"]:
        tmp = tempfile.mkdtemp()
        subprocess.run(["adb", "pull", ADB_PATH, tmp], check=True)
        path = pathlib.Path(tmp) / "collection.anki2"
    elif len(sys.argv) == 2:
        path = pathlib.Path(sys.argv[1])
    else:
        sys.exit(__doc__)

    db = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    daily, groups = snapshot(db)
    first, last = min(daily), max(daily)
    span = (last - first).days + 1
    total = sum(daily.values())
    # No blank lines: markdown ends a block of raw HTML at the first one.
    block = "\n".join([
        "<!-- anki -->",
        '<figure class="anki">',
        heatmap(daily),
        f"<figcaption>{total:,} Anki reviews on {len(daily)} of the {span} days from "
        f"{first:%B %-d, %Y} to {last:%B %-d, %Y}; the longest streak was {streaks(daily)} days. "
        f"Mature cards are ones I won't see again for three weeks or more.</figcaption>",
        "</figure>",
        table(groups, last),
        "<!-- /anki -->",
    ])

    text = TARGET.read_text()
    a, b = text.index("<!-- anki -->"), text.index("<!-- /anki -->") + len("<!-- /anki -->")
    TARGET.write_text(text[:a] + block + text[b:])
    print(f"{TARGET.relative_to(ROOT)}: {total:,} reviews through {last}")


if __name__ == "__main__":
    main()
