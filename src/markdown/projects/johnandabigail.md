---
title: "Letters of John and Abigail Adams Twitterbot"
url: "https://github.com/mas-4/johnandabigail"
featureImage: "./john_and_abbie.png"
short: "john"
category: "automation"
tags:
  [
    "python",
    "aws",
    "twitterbot",
    "netlify",
    "beautifulsoup4",
    "scraping",
    "civics",
  ]
---

This project was inspired by a [photo][11] that made the rounds of Twitter in
the wake of the protests in June 2020. The photo was of John Trumbull's famous
painting of the signing of the Declaration of Independence with red dots over
the faces of all the slave-owning founding fathers. Only 8 or 9 of the several
dozen men in the photo could boast never having owned slaves and John Adams was
smack dab in the middle with his face as apparent as ever.

I've always been a bit of a John Adams fanboy so I decided to put my Python to
work making a twitterbot that would tweet lines from the letters of John and
Abigail Adams, a lovely repository of romantic correspondence.

The bot tweets out fairly regularized sentences in threads that correspond to
each letter in chronological order, and then repeats. I used tweepy for the
Twitter interfacing, AWS's Lambda to run the program, and AWS's DynamoDB to keep
track of where the bot is. The actual letters are hosted on a static site of
json files on Netlify. That simplified some of the deployment for various
reasons I can't recall now.

- Twitter handle [@john_and_abbie][10]
- Bot to tweet the corpus of letters between [John and Abigail Adams][0]
- Data scraped from NARA's [The Adams Papers][1] using [requests][2] and
  [BeautifulSoup4][3]
- Use [AWS DynamoDB][6] to track place in corpus
- Use [Netlify][7] to host the letters as static text files

[0]: https://www.masshist.org/digitaladams/archive/letter/
[1]: https://founders.archives.gov/about/Adams
[2]: https://requests.readthedocs.io/en/master/
[3]: https://www.crummy.com/software/BeautifulSoup/
[4]: https://www.tweepy.org/
[5]: https://aws.amazon.com/lambda/
[6]: https://aws.amazon.com/dynamodb/
[7]: https://johnandabigail.netlify.app/1777-04-02-0-john.txt
[8]: https://urllib3.readthedocs.io/en/latest/
[9]: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
[10]: https://github.com/mas-4/johnandabigail
[11]:
  https://hyperallergic.com/572035/historical-painting-is-altered-to-show-most-declaration-of-independence-signatories-were-enslavers/
