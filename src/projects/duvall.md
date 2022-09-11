---
title: "Duvall Invitational Realtime Scoring Site"
url: "https://duvallinvitational.com"
featureImage: "./duvall.png"
short: "duvall"
category: "frontend"
tags: ["ssg", "sergey", "excel", "onedrive", "javascript"]
---
My father hosts a golf tournament every year known as the DuVall Invitational.
It's been running for over fifty years and is mostly played by men in the
construction industry and their friends. But as with everything, using the web
allowed them to improve the general quality of life in the tournament.

They use a master Excel spreadsheet to keep track of scoring, auction data, and
handicaps that is carried over from year to year. A year or two ago I made some
massive improvements to the software infrastructure they use.

First, I remade their spreadsheet from scratch, as it had become a crufty mess
of tangled code, with `IF(IF(IF()))` style formulas that stretched over a
hundred characters long with excruciatingly difficult logic. I upgraded them to
using the latest version of Excel which allowed me to program it using modern
Dynamic Arrays and Named Ranges. This made drop down selection a lot easier, so
that the list of options in a given cell could be checked against the sheet
itself to filter out used options.

I also created a standalone handicap spreadsheet that allows them to dynamically
calculate handicaps by weighting scores from the previous 5 years without having
to mess with moving columns and rewriting formulas.

Then I found the lightest-weight static site generator I could, [Sergey][0], to
generate a static site that used a little bit of JavaScript to make keeping
track of the API keys for the spreadsheet stored in Microsoft OneDrive easier.
The result is that my father only has to make changes to a spreadsheet that he
uploads to OneDrive and those changes will dynamically update on the webpage in
embedded frames that point to specific ranges on that spreadsheet. They find it
incredibly helpful to check up on how their competition is doing while out on
the course using their smartphones.

I even made a [PR upstream to Sergey][1] when I found that the development server
automatically exposes to the network using 0.0.0.0. Unfortunately, the
maintainer still hasn't merged it. Luckily, it's lightweight enough that I can
maintain the SSG myself without worrying about it being no longer maintained.

All the code for the site can be found at [mas-4/duvall][2].

[0]: https://sergey.cool/
[1]: https://github.com/trys/sergey/pull/52
[2]: https://github.com/mas-4/duvall
