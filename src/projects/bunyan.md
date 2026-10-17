---
title: "Bunyan"
url: "https://github.com/mas-4/bunyan"
featureImage: "/projects/bunyan.jpg"
short: "bunyan"
category: "mobile"
ai: "Built by Claude"
order: "05"
year: "2025 – 2026"
tags: ["dart", "flutter"]
---
Bunyan started as a minimalist logger: type a word, get a timestamped entry.
Why "Bunyan"? It's a logger. 🪓

It has grown into four screens, all built on that one log:

- **Log** is where anything new goes, from a quick note to a complicated
  entry. A small language in the entries feeds the other screens: `@tags`
  group things (`@dog`, `@workout`), and `@habit[...]` makes an entry a habit
  with a schedule: `@habit[1d]` for daily, `@habit[2/d]` for twice a day,
  `@habit[monday,thursday]` for particular days.
- **Habits** turns those entries into a grid of the last few days, showing
  what got done, what was missed, and what's still open today.
- **Stats** suggests what I usually log around now, so the routine entries
  are a single tap.
- **Todos** is a plain todo list.

Underneath, it's all one CSV of timestamped entries. Every screen is just a
view of it, so the whole history is always one file away from a spreadsheet
or a notebook.
