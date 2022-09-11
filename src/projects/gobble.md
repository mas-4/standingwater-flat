---
title: "gobble.py"
url: "https://github.com/mas-4/gobble"
short: "gobble"
category: "automation"
tags: ["security", "python"]
---
This was a one off quick project as a joke idea. It's a python script using the
`secrets` module from the Standard Library to generate a password including an
English word from the Electronic Freedom Foundation's [Diceware list][0]. It
produces passwords that look like this: `hydrant_34l;k1qjfasdf`.

The idea was to circumvent the ["gobbledy-gook" social engineering
vulnerability][1] in Security Questions. Some people just put a randomly
generated string for the security, but then the worry is that when an operator
on a phone asks for it, they'd just accept the answer "It's just a bunch of
gobbledy-gook". This script's idea is that if there's a single recognizable word
in the security phrase, the operator would hopefully at least require that.

A better solution would be to just use diceware, but where's the fun in that?

[0]: https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt
[1]: https://github.com/mas-4/gobble#background
