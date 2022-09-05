---
title: "Generated Anki decks"
url: "https://github.com/mas-4/minimalpairs"
featureImage: "./anki.jpg"
short: "anki"
category: "automation"
tags: ["python", "ibm watson", "beautifulsoup4"]
---
Learning French from English is sometimes tricky. Especially with recognizing
the difference between certain words, like au-dessous vs au-dessus (below vs
above). So I decided to generate an Anki deck with audio files pulled from
forvo.com's API that are distinguishable by a single phoneme (the ones I find
myself distinguishing). To read my process, please see the README in the [Github
repository][5].

The other deck, [the numbers deck][6], consists of 2500 audio files generated
through IBM Cloud's text to speech generator. It is the first 2500 numbers in
French with their corresponding words and numerical representation. It is
sometimes hard to understand French numbers because it uses a mixed
decima/vigesimal system (seventy is sixty-and-ten, eighty is four-twenties, and
ninety is four-twenties-and-ten).

These projects are simple, but I am proud of them. I seem to have helped a lot
of people learning French with them.

The minimal pairs deck, in particular, required a lot of strategizing for
dealing with the forvo.com api rate limits (500 requests per day) and the
combinatorial explosion of comparing minimal pairs.

- Generated an [Anki deck][0] for recognizing phonemes difficult to hear for an
  American English speaker using “[minimal pairs][1],” words in French which
  differ by only one phoneme using the forvo.com api. Almost 600 downloads and
  3 positive reviews.
- Also generated an [Anki deck][4] for training the ear to hear difficult French
  numbers (which use a mixed vigesimal, or base-20, system) using IBM Cloud's
  Text to Speech renderer and the num2words Python library. Over 500 downloads
  and 3 positive reviews.
- Used [Requests][2] for automated downloading of the audio files
- Used [BeautifulSoup4][3], requests for scraping the list of minimal pairs in
  an IPython session

[0]: https://ankiweb.net/shared/info/1347940877
[1]: https://en.wikipedia.org/wiki/Minimal_pair
[2]: https://requests.readthedocs.io/en/master/
[3]: https://www.crummy.com/software/BeautifulSoup/
[4]: https://ankiweb.net/shared/info/1704367316
[5]: https://github.com/mas-4/minimalpairs
[6]: https://ankiweb.net/shared/info/1704367316
