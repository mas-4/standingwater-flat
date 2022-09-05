---
title: "Poll Tracking"
url: "https://polling.netlify.app"
featureImage: "./polling.png"
short: "polling"
category: "automation"
tags:
  [
    "data",
    "civics",
    "netlify",
    "matplotlib",
    "pandas",
    "seaborn",
    "gatsby",
    "aws",
    "twilio",
    "requests",
  ]
---

During the 2020 election my friend and I were rapt with the polling changes.

I developed a couple of technologies to monitor changes:

1. A site that showed all of the individual polls to track changes within a
   given poll. This was displayed on a site [polling.netlify.app][0]. I had a
   [Jupyter Notebook][1] that would pull 538's polling data csv and parse it to
   create a ton of graphs that would then be pushed to the netlify/gatsby app.
2. A [script][2] that ran in AWS Lambda that would, every ten minutes, check
   538's topline polling projection and then text me and a friend every time
   there was a change using Twilio.

This stuff was a hell of a lot of fun. I expect once 538 launches the '22 model,
I'll be setting it all up again.

[0]: https://polling.netlify.app
[1]: https://github.com/mas-4/polling-site/blob/master/exploration.ipynb
[2]: https://github.com/mas-4/modeltexter/blob/main/modeltexter.py
