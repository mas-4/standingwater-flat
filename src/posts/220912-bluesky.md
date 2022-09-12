---
title: "Lessons from writing my own SSG"
date: "2022-09-12"
---

# Background

In May I lost my dog. Her name was Sky, and I memorialized her in the blog post
[On Death](220514-death.md). When I wrote that post, still fighting back tears
the day she passed, Gatsby, the framework my site was built on, refused to start
its development server on my machine. I wrote the post in neovim, pushed, and
hoped Netlify would render it. It did, but the experience left a sour taste in
my mouth. When I want to write, I don't want to have to deal with broken
dependencies.

So I thought, fuck it, I'll write my own SSG. It can't be too hard.

I decided to model it on an SSG I'd used for a simple web site I made a few
years back for my dad, [Sergey][sergey]. It's a wickedly simple SSG, that only
has two features: html partials (includes) and markdown rendering. I decided, in
my grief, to name it after Sky, my late dog. And I decided to write it in C.

After struggling for two weeks in C, I switched to C++ and reached feature
parity with the C implementation in a day. I struggled to advance beyond the C
implementation, paused for a few months, and restarted again two weeks ago,
finally reaching completion.

This post is meant to catalog some of the lessons I learned from writing
[bluesky][sky].

# bluesky basics

bluesky is a very simple static site generator, consisting of three basic
features:

1. `<bluesky-include>`: a means of dropping another html file whole cloth right
   into the calling file. The included file is also parsed, so includes are
   recursive.
2. `<bluesky-template>`: the inverse of an include, essentially a calling file
   can have named blocks which are dropped in their corresponding named slots in
   a template file. The template file is identical to a non-templated file,
   except that it has `<bluesky-slot>` tags for where a calling file should
   place its `<bluesky-block>`.
3. `<bluesky-markdown>`: A tag which will look for all markdown files in a named
   directory, generate html using a template and the markdown for each of those
   files, and create an unordered list of links to those pages in the calling
   file.

# Lessons

## 1. Avoid writing your own templating engine, if you're in a hurry

Long after I was months into working on the bluesky templating system, I decided
to google "write your own static site generator" and found a couple hits. They
all had in common:

1. They were not written in C/C++ (Python was common, as was JS, one was in
   rust).
2. None of them actually wrote their own templating engine.

The nature of the SSG I wanted (the absurdly simple templating bluesky has now)
required that I write my own engine, but that was a choice I made from aesthetic
reasons. I wanted something like sergey, only my own, and better (sergey doesn't
have templates, and, if I recall, can't generate a list of links to markdown
pages).

But it doesn't have to be that way. There are an insane amount of templating
engines that would be far easier to pop into a hand written SSG than to write
your own. There's one in C++ I eyed a little forlornly, [inja][inja], which is a
C++ implementation of the Python library jinja2, which I've used quite a lot. It
has a turing complete templating engine, including for loops and if statements.

So, if you really want to write your own templating engine, by all means, it's
not impossible, it's just harder than you might think at first.

## 2. Recursive page parsing is easier than a stack

On that note, I have a few recommendations about writing a templating engine.
First: do not try to be efficient.

My first implementation in C tried to be efficient. If I rendered a template
once, I didn't want to render it again. If I loaded a file, I didn't want to
load it again.

When I switched to C++ I decided that was stupid. Trying to make sure all the
includes and templates were parsed first, then the pages themselves, was a bit
of a chicken or the egg nightmare.

Because each file is dependent on an arbitrary number of other files, it is
quite difficult to determine which files to parse first. You start on a file,
recognize it requires a template, so you move to parse that. Then you recognize
an include in the template, so now you have to parse the include. This sort of
dependency chain is very hard to determine in situ, so its much better to just
write a class that can determine its own dependencies and parse them on its own.

I also remembered that modern operating systems have file caching. When you open
a file and load it into ram, it is cached by the OS so that subsequent reads of
the same file will read from memory instead of disk, which means opening the
same file multiple times will not be very expensive at all.

## 3. Multiple passes is way easier than one

In the same vein, I still tried to keep some efficiency by making only one
rendering pass per file. The basic pass worked like this: loop through the
contents looking for `<bluesky-`, my common opener. For each opener, identify
the tag, parse it, push the parsed text into a string stream.

What I found was that this became increasingly complex as I added tags. I only
have 3 features but that required 5 tags. And once I added markdown parsing it
became impossible.

Instead, I decided to start factoring stuff out, and the result is 3 passes on
the same file. The files are never very large for my own site, so it's still
incredibly performant. When I run the development server, if I touch any file in
the directory, the entire site rerenders (this was a deliberate choice). The
latency is unnoticeable.

Do yourself a favor, do multiple passes.

## 4. Don't shove all the functionality in one class

It also occurred to me at far too late a point that it was a bad idea to try to
parse a Template as a Page. This is probably Object Orientation 101, but I like
simple implementations that treat everything the same. However, even though a
Template can contain the same tags as a Page, the nature of the parsing and use
of the page is different, so trying to shoehorn them into the same class turned
out to be a disaster. Once I split the Template functionality into its own
class, it became much easier to write and use.

Actually, Templates in bluesky can't use the markdown tag, so they're not
equivalent anyway. Though this now seems like an arbitrary limitation I am
considering lifting. However, one thing I was not the biggest fan of was the
idea of recursive templates. It's not possible on bluesky currently, but I'm
hesitant to add that functionality.

## 5. You'll need a development server

If you want to work on a site with your own SSG, you're going to need a
development server. That means, you can run your program on your site, point
your browser to `localhost:8080`, make changes to a file, reload, and see the
changes immediately.

The other reason you want the dev server is because then your site will work
locally. Links don't work the same when using a `file:///` url. If your index
page is linked to with `<a href="/">home</a>`, clicking that link will take you
to a listing of your root directory. By serving the files, you can make sure
that the paths work appropriately to the links.

In C++ this meant socket programming. It was nowhere near as hard as I
anticipated, the entirety of my server code comes to [just 132 lines][server]. I
actually tried reading way more than I needed to before attempting to write a
simple hello world, all I needed was [this helpful guide from Skrew Everything
on Medium][se].

The trickiest thing, which I am still trying to improve, is the hot reload,
which is the harder part of the dev server. This consists of two parts:

1. When a file changes in your `src` directory, regenerate that page.
2. When the page your browser is pointed to regenerates, refresh the browser.

I only have 1 working right now, and it's far simpler than my initial attempt.

The first thing to know about file monitoring is that polling can be very
resource intensive so its a bad idea to just loop and poll constantly for last
modified times. There are system apis to do that without polling. However, they
are very different in different OS's, so its best to use a library if you want a
cross platform solution. I didn't want to use a library, and I didn't want to
constantly poll, so I did something simpler.

Only when a browser makes a request to bluesky, bluesky loops through and polls
all the files in the source directory (_all of them_, not just rendered pages,
but images and binaries as well), and checks if any of the last modified times
are younger than what are stored in a hash map. If a single one is, the entire
site is regenerated. There are 80 files in my source directory currently. I do
not notice any latency in the browser when the entire site regenerates. It is
incredibly fast.

At first I tried just rerendering the page I was on, but realized that the
dependency pages could change and the current page wouldn't update. I tried
fixing this by adding a list of paths to all of the files that each page used as
a dependency and checking those as well. But then I realized that the page also
depends on files my system didn't parse or touch, except to copy, like a css
style sheet. So I changed to checking every file in the directory. It still
doesn't know about new files, which is something I'd also like to try changing.
It seems like a simple fix: don't loop through the hash map, loop through the
files in the directory; if there's one not in the hashmap, rerender. I'll get to
it soon enough.

As for the browser refreshing, I've done similar things before in web apps I've
worked on, and it's fairly simple: inject some javascript. I was hoping there
would be a simple javascript api for monitoring a file system, but alas, there
is not, because of security; so to do it I'd have to spin off a thread in
bluesky with an endpoint for the javascript to poll to check the last modified
time to result in a refresh. So I've abandoned it. For now, I can refresh after
I make a change. It's not that much work.

## 6. Do not write your own markdown parser

One thing I can say without a doubt, if you intend to write your own templating
engine, do not under any circumstances take it upon yourself to write your own
markdown parser. I never tried, but judging by the code of md4c (the parser I
chose to use) it is incredibly complex. I did not imagine that would be the
case, because markdown is so simple, but md4c has so many lines of code that,
with just the 3 basic necessary files I included for its use in bluesky, Github
says my project is 80% C.

md4c is a really cool library. It's definitely fast, but the C style is also
very cool, including the use of callbacks. The documentation is lacking, but
there was an example file that was easily adaptable.

## 7. Write it for yourself

When I initially started, I had typical dreams of grandeur, that I was writing
an open source project others would find useful. As time went on, and I saw that
a lot of people write their own SSGs, I realized I shouldn't worry about that. I
just wanted to write it for me, and for my dog. It feels really good to see her
name everywhere as I'm working on my site.

So my advice is just that: don't write something you think someone else will
use. Write it for yourself.

If anyone reading this is interested in trying out bluesky, I am more than happy
to help you get started. I'm quite proud of the result. I just don't have any
expectations of anyone using it.

Though, sergey has users, and I have more features than sergey, so who knows.
Maybe people will like it.

# Afterword

I've been working in Python for 5 years now. Toptal labelled me a "Python
Expert" so I feel comfortable saying if I can do something, I can do it in
Python. I chose to do this project in C then C++ because I wanted to exercise
those memory handling systems programming muscles, and this project offered
enough of a challenge to start feeling much more comfortable writing C++ (C too,
actually).

That being said, the difficulty in writing bluesky did not lie in the choice of
programming language. Sure, string handling is a lot easier in Python, but
templating is hard anyway. At one point, so frustrated trying to get my Template
system to work, I switched to Python to write a proof of concept, figuring I
could get it done in 5 hours and see how to write it in C++.

That was not the case. It was just as hard in Python as it was in C++.
Templating is hard. Period. I've done a considerable amount of text processing
in programming. One of my first projects was a web app for annotating classical
texts, which involved parsing Project Gutenberg text files; I wrote the text
processor _twice_. And _still_ templating is hard.

So, I'm not saying its not a worthwhile endeavor, but you have to want to do it.
I _really_ like sergey, and _really_ wanted to stop depending on it. I also
_really_ wanted to finish something in tribute to my dog. This was my first
major personal project in years. And I'm really proud of it. I hope someone else
can learn from it. Maybe someone can even build something with it.

[sergey]: https://sergey.cool
[sky]: https://github.com/mas-4/bluesky
[se]:
  https://medium.com/from-the-scratch/http-server-what-do-you-need-to-know-to-build-a-simple-http-server-from-scratch-d1ef8945e4fa
[server]: https://github.com/mas-4/bluesky/blob/main/src/Server.cpp
[inja]: https://github.com/pantor/inja
