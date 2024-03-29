---
title: "languageMap.js"
date: "2020-06-22"
---

Some time ago, while I was learning French and perusing language resources like
[r/languagelearning][0], there was a meme whereby Redditors would post pictures
of world maps with the countries colored in whose languages they could speak. It
was a kind of way of seeing how much of the world was open to you.

At the time I was just starting to learn a little bit of React and Gatsby and I
thought it would be really cool if there was a simple app that could generate
these maps. I figured I could do it in React. [I even made a comment suggesting
I'd been thinking about doing it.][1]. It ended up getting 31 upvotes, so I feel
a little bad that it took me eight months to get around to doing it. But I
finally did.

This blog post is to serve as a little insight into how much effort ended up
going into it, and where I plan to take it down the road. Most of it is actually
about the data gathering process because that was the most interesting, and
difficult.

## The Skeleton

The very first thing I do when I start a new project is build a skeleton of the
project and get it hosted. I have had enough experience banging my head against
a wall trying to deploy a finished project to know that it's best to get that
out of the way in the first place. I prefer to develop with the deployment
pipeline already built.

As such, the first thing I did was find a library for displaying maps in react.
I found a beautiful one in [React Simple Maps][2]. They are as simple as, I
imagine, a map can be in a programming language. I copied the code from their
[Choropleth map chart example][3], got it set up as the base for the app,
figured out how everything fits together, switched to a [topojson file without
Antarctica][4] because Antarctica is literally useless for my purposes, messed
around with different projections (I understand the racist implications of the
Mercator projection but I chose it anyway because most of the languages that
people learn are in Europe and the northern hemisphere), and deployed the app to
Netlify.

After all that was done, it was time to get the data.

## Data Gathering Part I

I don't know why I always think that data will be easy to find and gather, but
in this case it most certainly was not.

I needed a list of countries ordered by languages, _not_ languages by countries,
as is viewable in [this Wikipedia article][5]. Actually, damnit, now that I
think about it, in retrospect, I probably could have used that article and it
would have ended up being more normalized; still might update my data that way.

The only two resources I found that fit the bill were [this other Wikipedia
article titled List of countries by spoken languages][6] and this [page's
subpages][7] that even provide distributions. In examining the two I decided
that I'd go with the second resource, on WorldData.info, for two main reasons:

1. WorldData.info's data was considerably more normalized and well-formatted
   than the Wikipedia data.
2. WorldData.info's data included a 'Distribution' column, and from the example
   on react-simple-maps.io I'd copied I had the ability to do heat maps. I
   thought that would be pretty darn cool.

So I set to installing BeautifulSoup4 and requests and opening up an iPython
session to start ripping the data and formatting them into a pandas data frame.
Right away I ran into trouble.

Before I started this project I'd thought I already knew everything I'd ever
need to know about web scraping if I never became a professional scraper. I
learned immediately that I was wrong.

The very first issue I had was that I got a 403 when I requested the main index
page. A quick Google and the number one suggestion was that I'm not setting my
user-agent header. So I found a list of common user-agent headers and started
using that and everything worked swimmingly.

I formatted the links and languages from the index into a dictionary and wrote a
little for loop to GET all the pages corresponding to each language and print
out the status code as it went. I even went so far as to add a
`time.sleep(random.randint(1,6))` to try and space out the requests.

Everything went well until I got to around the 8th page. Then I got a 429. Too
Many Requests.

Crap.

Now I started googling proxies and requests. I'd never had to do it before but
I've always known you could, and it turns out there are a wealth of free and
cheap proxy services that will give you plenty of free proxies to hit a site
from. I specifically came to like [pubproxy.com][8], which provides an API that
gives you a proxy every time you call it (rate limit of 50 per day, of course).
So I wrote a new for loop, probably wasting about 10 requests as I developed the
code to query it and test it out, and set it to run.

There are things in life that everyone is told, everyone knows, and make
perfectly good sense, like "never email a password in plaintext even to
yourself", but that, when we're trying to get something done quick, we don't
always heed.

"Never write a naked try...catch clause" is another one. And on Saturday night I
learned exactly why.

When I set the for loop querying pubproxy to running, I figured I had about
30-40 pubproxy requests left for the day, and there were only about 15 pages on
WorldData.info that I had to rip, so I'd be good to go. It was running fine, at
first. It would get a 403, then a 200, then a 429, then a 200. It was fine. Then
it hit 429, 429, 429, 429. I figured something might be wrong so I Control-C'd
the script to stop it. Nothing happened. I Control-C'd several more times. Still
nothing. Then it dawned on me.

I was silencing the KeyboardInterrupt.

I had to kill the entire iPython session and lose all the data that I'd already
gathered. All the first 8 pages I'd ripped PLUS the actual links to all the
pages I'd still have to rip.

And to top it off, after I restarted iPython I discovered that I'd already hit
the rate limit for the day on PubProxy and I'd have to find a new proxy service.
Oh well. Live and learn.

Anyway, I found [scrapestack.com][9], which turned out to be way more convenient
anyway. With 10,000 requests per day (iirc) and no need to configure and store
proxies or user-agents, it was way quicker and easier than using pubproxy.
Basically, you just request a page through their service and they scrape it for
you using their own internal proxies and user-agents. I got all 20 or so pages
in one go with that.

---

After scraping it all (which basically took all of Friday night—there's not much
to do during the pandemic) formatting it was fairly easy, and then I started
messing around with the react site. And that's when I started getting
disappointed with the WorldData.Info data.

It really only includes the top 30 languages by number of speakers in the world.
Which is of course a logical thing to do, considering there are some 5,000
languages in the world and you've got to cut if off at some point, but the
result is a list that doesn't at all fit the niche purposes of the app. I'm
trying to make it useful for the r/languagelearning nerds, and they like
learning both off-the-wall hipster languages like Uzbek (which is, like, [a meme
on r/languagelearning][10]) and smallish traditional one-state languages like
Norwegian or Vietnamese.

So, in reality, I had to do the Wikipedia page.

## Data Gathering Part II

The Wikipedia page in question required a lot of by-hand intervention. I started
by using [this nice .de site][11] that converts all the tables on a wikipedia
article to nicely formatted csv's. I went through and downloaded them all, to be
concatenated into one big csv with some editing, but discovered pretty quickly
that the download option on that site corrupts some of the Unicode characters.
Since I didn't want to copy and paste and save and re-open excel 53 times (there
are 53 tables) I gave up and went searching for a new solution.

There are a number of resources for doing this, but the one that I was most
shocked by was Google Sheets. Some googling dropped me on [this lovely answer on
opendata.stackexchange.com][12] that talks about `=importHTML()` in Google
Sheets. I tried it out and it works incredibly. My next step was to find out how
to automate the import for all 53 tables. Turns out there's a library for
automating Google Sheets: [gspread][13]. So the Wikipedia page turned out to be
way easier than I expected.

I used gspread to automatically generate 53 worksheets in a single spreadsheet
with variations only on the table number. Something like this did it for me:

```
for i in range(1, 54):
    worksheet = spreadsheet.add_worksheet(title=str(i), rows="100", cols="10")
    worksheet.update('A1', f'=importHTML("https://en.wikipedia.org/wiki/List_of_countries_by_spoken_languages", "table", {i})')
```

And that was literally it. I copied and pasted each table into a new
spreadsheet, updating the language column based on whether it was a table of
families of languages or just a single language, and used gspread to eliminate
some of the artifacts (like asterisks and bracketted numbers) automatically.
Then I made a new copy (gotta version control, even in Google), and normalized
all of the language statuses to a mere 10. Found a list of all the ISO Alpha-2
country codes, used pandas to pivot on a country column, re-uploaded to Google,
fixed the missing country codes, and that was it. I wrote a [quick script to
generate a json file][14] (really it generates a js file which exports a
javascript object but what's the difference) and I was good to go.

## Finishing the App

Building the app was a lot easier than I expected. Honestly, there's not much to
say about it. I used material ui for the checkboxes, then I discovered how awful
the response time was with some 500 check boxes on one page so looked into
alternative input options. Luckily material ui has a great set of [Autocomplete
components so I ended up using one of those][15]

And then it was done. I bought a \$15 domain name for it,
[language-map.com][16], and hosted it up on netlify. For some reason I had some
trouble with the dns clearing but it worked out this morning.

So anyway, that's it, my dramatization of this past weekend. I am going to post
about it sometime this week on r/languagelearning and hopefully I get a
response. We'll see though. Then I want to work on my next project, a twitter
bot that tweets lines from the letters of Abigail and John Adams. [It seems John
has been having a bit of a moment][17] and I've always been a super fan so when
I searched for John Adams on twitter and found no real representation I decided
to make a bot. That'll probably be my next write up.

I'd also like to eventually post some stuff on my dotfiles set up. We'll see.

[0]: https://www.reddit.com/r/languagelearning/
[1]:
  https://www.reddit.com/r/languagelearning/comments/dmeea5/map_of_the_languages_i_speak_rmapporn_xpost/f4zxvf3/?context=3
[2]: https://www.react-simple-maps.io/
[3]: https://www.react-simple-maps.io/examples/world-choropleth-mapchart/
[4]:
  https://github.com/mas-4/topojson/blob/master/world-countries-sans-antarctica.json
[5]:
  https://en.wikipedia.org/wiki/List_of_official_languages_by_country_and_territory
[6]: https://en.wikipedia.org/wiki/List_of_countries_by_spoken_languages
[7]: https://www.worlddata.info/languages/index.php
[8]: http://pubproxy.com/
[9]: https://scrapestack.com
[10]:
  https://www.reddit.com/r/languagelearningjerk/comments/gt7h7o/do_you_only_know_one_joke_youll_love_ruzbek/
[11]: https://wikitable2csv.ggor.de/
[12]: https://opendata.stackexchange.com/a/828
[13]: https://gspread.readthedocs.io/en/latest/
[14]: https://github.com/mas-4/languagemap_data/blob/master/generate_json.py
[15]: https://material-ui.com/components/autocomplete/
[16]: https://language-map.com
[17]: https://twitter.com/jbf1755/status/1274018121716764672
