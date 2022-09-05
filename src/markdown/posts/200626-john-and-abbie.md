---
title: "lambda_function.lambda_handler"
date: "2020-06-27"
---

I made a bot. [@john_and_abbie][0].

It tweets lines from the letters of John and Abigail Adams. All of them. In
order. It should take a bit over 109 days to loop. If I did my math right, there
will be 15,799 tweets, every 10 minutes, which is about 2,633 hours, or 109ish
days.

It was rough. A lot rougher than it probably is for most bots, mostly because I
was developing for AWS. In fact, abut 70% of getting this project to work was
working with AWS. I learned a LOT.

---

I do not know if AWS is as simple as it can be, or if it's just that it offers
such a bewildering array of products that it makes things necessarily
complicated, but it is jaw dropping how difficult it can be to do something as
simple as run a script every ten minutes. One of the problems with figuring out
whether it actually is overly complex, or just necessarily complex, is that the
complexity becomes shockingly transparent once you understand what you're doing.

Take the title of this blog post. I was initially fairly confused about how to
get a lambda function to run. I uploaded a zip file with my script and figured
there'd be somewhere to enter a run command. That wasn't the case. I started a
new test lambda function and saw that I'd overwritten a file called
`lambda_function.py` with a function called `lambda_handler()`. So I copied the
code into my git directory, wrote a line of invocation code, and it still didn't
run. I had to realize that I was literally just dealing with a Python package
and that the reason `lambda_function.py` could not be imported by the system was
because it wasn't packaged. So `touch __init__.py` and upload. It ran.

The next problem that was a little obvious in hindsight was how to authenticate
my script to my DynamoDB table. None of the tutorials seemed to explain that,
they just showed `dynamodb = boto3.resource('dynamodb')`, but whereas I'm used
to having to submit authentication keys and uri strings, apparently this is not
at all the case with DynamoDB on the system. Any resource on AWS can access any
other resource without authentication. I had to install the AWS cli and
authenticate my computer to access those resources while developing on my
computer, but that's transparent once it's done.

A third sticking point was how to package dependencies. And even _that_ was far
more easy than I'd expected. Lambda automatically exposes `Boto3` and `urllib3`
(so I switched to `urllib3` in the script from my preferred `requests`; I'm
going to investigate `urllib3` more now, though, because I'm always interested
in new libraries) so those don't have to be packaged. As for `tweepy`, that was
as easy as a `pip install tweepy -t ./` to install the library to the base
directory of my git project, and then just zipping it all together.

The final sticking point was getting the permissions for my lambda function to
access the DynamoDB table. That didn't turn out to be overly difficult, either.

Learning any new platform can be confusing and frustrating. I remember getting a
little upset with Heroku in the beginning but ended up finding it to be pretty
easy once I got the hang of it. There were more than a few times, as I got going
with AWS this time around (my only previous experience was with an ec2 instance
for [vote.py][3]) where I growled in frustration at having to learn something,
and something else to get it to work, and something else to get _that_ to work
(the full chain of dependency seems like this: Cloudwatch -> Lambda ->
Permissions Policy -> DynamoDB). It began to feel a bit like [dependency
hell][1]. But I guess, at the end of the day, that's just how you start to break
into a complex system of microservices. You have to yakshave with dependency
hell for a little bit before you feel comfortable.

After all that, I can say I kind of like AWS. Kind of, I say, because one thing
I was and continue to be bothered by is the lack of git integration. With
Netlify and Heroku git is (or can be) a principle part of deployment. This is a
very developer-first attitude. There are so few developers that _don't_ use git
that it feels almost like a given that a modern serverless system will allow
deployment via git. But not AWS. It's deployment via zip, and I'm not the
biggest fan. It took all of a minute to write a simple [Makefile][2] to automate
the process, but I would still prefer to just use git.

Anyway, follow my bot.

[0]: https://twitter.com/john_and_abbie
[1]: https://en.wikipedia.org/wiki/Dependency_hell
[2]: https://github.com/mas-4/johnandabigail/blob/master/Makefile
[3]: /20200611-100614/
