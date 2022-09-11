---
title: "teamup.py"
url: "https://github.com/mas-4/teamup"
short: "teamup"
category: "automation"
tags: ["combinatronics", "python"]
---

This script came about because of a family tradition of playing Christmas
Trivia. The idea was to create a computerized method for achieving the closest
balanced teams of arbitrary size and number.

It takes a JSON file with team members and their skill level (this could be any
numeric scale, like 1-10, 1-100, whatever), and then uses a generator to get the
best match up over time. That is to say, it looks for the next best teams
continuously. There's a huge diminishing return on calculating combinations, and
it's extremely computationally expensive to calculate all the possible team
combinations, but after about five to ten minutes you get pretty good team
arrangements, better than if you just did it by hand.
