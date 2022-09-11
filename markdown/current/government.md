---
title: "government.py"
url: "https://github.com/mas-4/government"
short: "government-sim"
category: "datascience"
tags: ["python", "numpy"]
---

I had a wild idea one day on the way to work: what if you used OOP to build a
government simulator. You could test the relative conservativeness or
liberalness of governmental structures themselves.

Everything is composed of Voters and Laws. Voters decide between Laws in
elaborate structures we call "institutions". So I built a library that
represents Voters and Laws as points in n-dimensional political space.

If a law's political position in that space is too far from the voters (i.e.,
the distance between the voter's point in political space and the law's
position) is greater than the voter's compromise distance (a single number
rather than an n-tuple coordinate point), then the voter votes no. Else, yes.

From there we build constituencies, offices (that are really just a voter
elected by their constituency), political bodies (i.e., legislatures), and
so-on, and so-forth. Run simulations, see what percentage of laws get passed.

It's been about a week since I hacked on it, and there's a bug that means the US
passes every single law, but we're getting there. I'd like to run simulations on
different distributions of political positions: right now it's Belle Curve
shaped. I'd like to see what happens if political positions are Well Curve
shaped (i.e., polarized).
