---
title: "Intertextual Canon Cloud (anno.wiki)"
url: "https://github.com/Anno-Wiki/icc"
featureImage: "./annowiki.png"
short: "annowiki"
category: "fullstack"
tags:
  [
    "python",
    "javascript",
    "flask",
    "etl",
    "heroku",
    "mariadb",
    "elasticsearch",
    "sqlalchemy",
    "jinja2",
  ]
---

The ICC is a web application designed to allow for collaboratively building an
exhaustive and definitive repository of annotated literature. I designed,
developed, deployed, and continue to maintain the project solo, managing
occasionally to rope in some programmer friends for help with various
features.It consists of ≈14k lines of code and ≈100k lines of code churn. The
backend uses Flask/SQLAlchemy. The frontend uses Jinja2, Sass, and VanillaJS. I
also had to write several ETL data pipelines for processing Project Gutenberg
texts. It is deployed via Heroku. I learned the entire web application life
cycle on this project, and it continues to teach me. It is currently maintained
at [https://anno.wiki][0]. I am also currently working on a second iteration of
the site.

- Wrote many [ETL data pipeline scripts][3] for processing [Project
  Gutenberg][4] text files into custom JSON formats
- [Heroku][5] for platform
- [MariaDB][6] for database
- [Elasticsearch][7] for search
- Vanilla JavaScript for AJAX and progressive enhancements
- [Talisman][8] for CSRF security
- [pytest][9] for testing
- [WTForms][10] for forms

[0]: https://anno.wiki
[1]: https://flask.palletsprojects.com/en/1.1.x/
[2]: https://www.sqlalchemy.org/
[3]: https://github.com/mas-4/texts/tree/master/processor
[4]: http://www.gutenberg.org/
[5]: https://www.heroku.com/
[6]: https://mariadb.org/
[7]: https://www.elastic.co/
[8]: https://github.com/GoogleCloudPlatform/flask-talisman
[9]: https://docs.pytest.org/en/latest/
[10]: https://wtforms.readthedocs.io/
