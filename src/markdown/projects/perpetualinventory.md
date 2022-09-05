---
title: "Perpetual Inventory"
url: ""
featureImage: "./shipping_container.jpg"
short: "pi"
category: "fullstack"
tags: ["react", "javascript", "jquery", "flask", "sqlalchemy", "materialize css", "celery", "redis", "postgres"]
---
One of the first projects I did for [HtmMbs][0], JP, the owner, wanted a way to
better manage inventory counts.

The system was built in Flask and SQLAlchemy with a LOT of JavaScript. I
designed a sophisticated admin panel (the bulk of the project) and a count queue
that could be put in multiple modes for various warehouses. The queue would
present a location and SKU for a warehouse worker to count, check how far off
their count was from what the system knew, occasionally ask for them to recount,
and keep track of whether or whether not the counts were consistent.

Because the company uses Odoo for everything, I had to write a lot of logic in
celery to keep everything synced. Adding a module to Odoo wasn't preferrable
because (a) this was a very heavy duty application, around 10kloc, and (b) every
new module in Odoo just makes the next migration that much harder. Better to use
separate services.

Among the features I added:

- An emergency queue and quasi-messaging system for communication between
  managers and admins to see if locations were being properly allocated and
  counters were consistent.
- A location allocation system.
- A picking allocation system in React that had a responsive map for allocating
  special picking locations.
- EOD reports for admins containing detailed statistics about the day's
  business.


[0]: https://mbs-standoffs.com
