---
title: "c′ and skyblue"
url: "https://github.com/mas-4/cprime"
featureImage: ""
short: "cprime"
category: "tooling"
ai: "Built by Claude"
order: "04"
year: "2026"
tags: ["c", "compilers", "static site generator"]
---
c′ (c-prime, the derivative of C, so its files end in `.dcdx`) is a language
idea I had in 2023: C plus the smallest possible version of classes. Structs
get methods, the receiver is called `ego`, and `.` and `->` mean the same
thing. Here's a Hello, World:

```c
#include <stdio.h>

struct Greeter {
  char *name;
  void greet(void);
};

void Greeter.greet(void) {
  printf("Hello, %s!\n", ego.name);
}

int main(void) {
  struct Greeter g = {"world"};
  g.greet();
  return 0;
}
```

In October 2026, Claude built it at my direction.
[cprime](https://github.com/mas-4/cprime) is a c′ compiler forked from Rui
Ueyama's [chibicc](https://github.com/rui314/chibicc). It's written in c′
itself, bootstraps from a frozen C copy, and checks that every stage compiles
the compiler to identical assembly.
[skyblue](https://github.com/mas-4/skyblue) is [bluesky](/projects/bluesky)
rewritten in c′ as a small compiler (lexer, parser, renderer), and it's what
builds this site now. The projects page you came from is, more or less, this:

```html
<sky-template path="main.html" />

<sky-block name="title">Projects · </sky-block>

<sky-block name="content">
  <h1>Projects</h1>
  <div class="cards">
    <sky-markdown directory="projects" template="project.html"
                  item="card.html" sort="order" />
  </div>
</sky-block>
```

`main.html` is the layout, with a `<sky-slot>` for each block; every markdown
file in `projects/` becomes a page through `project.html`, and a card through
`card.html`.

The ideas are mine; the code is Claude's.
