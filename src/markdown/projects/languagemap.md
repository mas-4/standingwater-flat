---
title: "Language Map"
url: "https://language-map.com"
featureImage: "./languagemap.jpg"
short: "languagemap"
category: "frontend"
tags: ["python", "react", "beautifulsoup4", "scraping", "data", "pandas"]
---
This project was inspired by a trend on [r/languagelearning][11] where
people would post world maps with the countries colored by the languages they
spoke. I decided to build an actual dedicated web app that would automatically
color the countries themselves.

To do this required a lot of data gathering and cleaning. Doing that itself was
an arduous process that had a lot of false starts. The final method I settled on
was to use Google Sheets `importhtml` function, which could be used to import
Wikipedia tables to a spreadsheet. To automate this I used Python and gspread.

It was definitely a lesson in data gathering and cleaning.

- Extensive data gathering and web scraping mission detailed [here][0]
- [BeautifulSoup4][1], [requests][2], [PubProxy][3], [scrapestack][4]
- [gspread][5], [Google Sheets API][6]
- [pandas][7], csv, json
- [ReactJS][8]
- [React Simple Maps][9]
- [Material-UI][10]
- Hosted on [Netlify][11]

[0]: https://blog.standingwater.io/20200622-151403/
[1]: https://www.crummy.com/software/BeautifulSoup/
[2]: https://requests.readthedocs.io/en/master/
[3]: http://pubproxy.com/
[4]: https://scrapestack.com/
[5]: https://gspread.readthedocs.io/en/latest/
[6]: https://developers.google.com/sheets/api/reference/rest
[7]: https://pandas.pydata.org/
[8]: https://reactjs.org/
[9]: https://www.react-simple-maps.io/
[10]: https://material-ui.com/
[11]: https://www.netlify.com/
[12]: https://reddit.com/r/languagelearning
