---
title: "ask.fiteyes.com"
url: "https://ask.fiteyes.com"
featureImage: "./fiteyes.png"
short: "fiteyes"
category: "backend"
tags: ["django", "postgres", "celery"]
---

This web application was built upon [Biostar][0], an [open source question and
answer framework][1].

The project consisted of several phases:

1. Researching the best base software to build a community upon. We considered
   several wordpress plugins as well as [Codidact][2], even going so far as to
   build a feature matrix comparing 20 solutions.
2. Launch consisted of modifying most of the templates and building a bit of
   infrastructure on a VPS.
3. Finally, continued development included adding a number of features,
   including more granular permissions, accessibility features, and making a lot
   of the site more abstracted to be suitable for launching multiple instances
   using the same code branch.

- [Nginx][5] and [Ubuntu][6] for the infrastructure
- Several JavaScript frameworks for quality of life features

[0]: https://www.biostars.org/
[1]: https://github.com/ialbert/biostar-central
[2]: https://codidact.org/
[3]: https://www.djangoproject.com/
[4]: https://www.postgresql.org/
[5]: https://www.nginx.com/
[6]: https://ubuntu.com/
