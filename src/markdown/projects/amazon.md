---
title: "Amazon BuyBox Notifier"
url: ""
featureImage: "./amazon.jpg"
short: "amazon"
category: "automation"
tags: ["python", "beautifulsoup4", "postgres", "elasticsearch", "data"]
---
This project was for a client who sells various vitamins on Amazon. I developed,
and redeveloped over several successive weeks, a rather large web scraping/api
scraping system that gleans information about Amazon Marketplace Offers on
products the client is selling from multiple data sources.

Because of the increasing complexity of the project it ended up becoming rather
large, with a decent amount of features:

- multithreading capabilities
- a token tracking system to make sure to stay within the rate limit
- header spoofing and proxy rotation
- near real time updates for various settings including which ASINS to track and
  notification endpoints using cloud file storage
- a PostgreSQL database for tracking data (using SQLAlchemy as the ORM, of
  course).
- database synchronization with an Elasticsearch instance for a Kibana dashboard

The software was deployed to an Arch Linux VPS and used a Systemd Unit to run.
I've done automated data gathering (mostly api/web scraping) before, but never
on this level. I had a lot of fun, building from the ground up. I'm especially
glad for having learned to do multithreading at a decent level.
