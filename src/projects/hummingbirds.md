---
title: "Hummingbird feeder tracker"
url: ""
featureImage: "/projects/hummingbirds.jpg"
short: "hummingbirds"
category: "science"
ai: "Built by Claude"
order: "06"
year: "2026"
tags: ["python", "tkinter", "matplotlib"]
---
I wanted to know how many hummingbirds were visiting my feeders. Counting
them is hopeless, so instead I log what I can measure (each feeder's weight
or nectar level, the time, what the birds were doing) and a small desktop
app works out the rest:

- **Consumption** from the change in weight over the nectar's density,
  cross-checked against the drop in level wherever there are both.
- **Bird counts** from 3 to 7 ml of nectar per bird per day, carried
  through as a range instead of averaged into one confident-looking
  number, because that rule of thumb is the biggest uncertainty in it.
- **Feeding time** measured to civil twilight, not by the clock, since
  hummingbirds sleep through the night.
- **Spoilage** accumulated hour by hour from the local temperature, pulled
  from Open-Meteo.
- **Seasonality** for the region from GBIF's bird records, divided by all
  bird records for the same week, so that it measures birds rather than
  how many people were out looking.

It was the first thing I built with Claude Code's ultracode, its
multi-agent mode.

Above: the Charts tab, comparing my feeders' season (orange) with ten years
of the region's ruby-throated hummingbird records (blue).
