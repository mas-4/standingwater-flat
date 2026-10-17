---
title: "bluesky"
url: "https://github.com/mas-4/bluesky"
featureImage: ""
short: "bluesky"
category: "tooling"
ai: ""
order: "03"
year: "2022"
tags: ["c++", "c", "static site generator", "md4c"]
---
bluesky is the static site generator I wrote in 2022 to build this site. When
my dog Sky died that May, I sat down to write about her and Gatsby's
development server refused to start. So I wrote my own generator, modeled on
the wonderfully simple [Sergey](https://sergey.cool/), and named it after her.

It does three things: includes, templates with named slots, and directories of
markdown turned into pages with a list of links to them. I started it in C
([bluesky-c](https://github.com/mas-4/bluesky-c)), struggled for two weeks,
switched to C++, and finished it that September. It built this site until
October 2026.

In 2024, while reading *Crafting Interpreters*, I rewrote it in C as
[nowclaire](https://github.com/mas-4/nowclaire), to try out the scanning and
lexing I was learning. Its successor, [skyblue](/projects/cprime), was
rewritten in c′ by Claude.
