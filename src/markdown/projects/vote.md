---
title: "vote.py"
url: "https://github.com/mas-4/vote"
short: "vote"
category: "automation"
tags: ["twilio", "aws", "python", "civics"]
---
A friend of mine had never voted, nor registered to vote. So I made sure she did
in 2020 by writing this little script to text her using Twilio to remind her to
vote on an increasingly frequent basis as the deadline for registration drew
near. She registered pretty quick, actually and it didn't run for that long.
Which is lucky, because I ended up discovering a breaking bug on the month roll
over.

I ended up having to resort to good old fashioned wheedling and emotional
manipulation to get her to actually vote, because she ended up just blocking the
number.

- Automated Python script to encourage and remind people to register to vote.
- Deployed using [AWS EC2][0] instance to enable continuous service.
- Integrated [Twilio][1] as texting client.
- Dynamic scheduling using `datetime` and `sched`

[0]: https://aws.amazon.com/ec2/
[1]: https://www.twilio.com/
