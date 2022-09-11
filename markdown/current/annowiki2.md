---
title: "icc2 / anno.wiki 2"
url: "https://wiki.anno.wiki/"
short: "annowiki2"
category: "fullstack"
tags: ["react", "javascript", "flask", "elasticsearch", "sqlalchemy", "postgres"]
---

This is the second iteration of the ICC (see projects), with improved data
architecture and a single-page application front end based in React. Using
Elasticsearch to store texts and PostgreSQL to store annotations and general
application data allows for faster incremental searching. I also wrote more
sophisticated text processors for breaking text into 100k byte chunks and
annotating stylistic elements, while stripping all styling from the raw text.

Annowiki is something I've been working on for four years now. I'll probably
never stop, and hopefully one day it will be more than just an intellectual
exercise.
