---
title: "A Minor C++ Performance Insight"
date: "2022-08-27"
---

# A Simple Optimization

A common data structure in C++ is the vector, which is a misnamed variable
length array.

Here's a simplified common bit of code you might see:

```c++
void append(size_t n, std::vector &vec) {
  for (size_t i = vec.size(); i < n; i++) {
    vec.push_back(i);
  }
}
```

I see this a lot, we all see this a lot, because programmers are lazy and don't
think about memory allocation.

Why is this bad? Because `Vector::pushback` checks to see if
`vec.capacity() == vec.size()` and then reallocates the entire array if true.
You might reallocate multiple times in this loop depending on n, and you \_know*
`n`, so you may as well allocate the memory once, at the beginning.

```c++
void append(size_t n, std::vector &vec) {
  size_t sz = vec.size();
  vec.reserve(n);
  for (size_t i = sz; i < n; i++) {
    vec.push_back(i);
  }
}
```

This is a pretty simple example, but I got in a discussion at work about it
because it was discussed in [This 2014 CppCon Talk][2014] by Chandler Carruth,
one of the project leads on the new [Carbon Language][carbon].

Specifically, I was bothered by the fact that Carruth, [who is an expert on
compiler optimization][2015] was recommending it. I expected that the compiler,
which I worship like a God, could have made that change for you. Apparently not.

My boss, on the other hand, said he wouldn't trust anyone making that
recommendation. He said you should use resize and bracket notation assignment.

I spent about 30-45 minutes with a co-worker trying to understand why resize
would be faster than reserve and missed the forest for the trees.

## Allocation

There are two steps in both my boss's recommendation

```c++
void append(size_t n, std::vector &vec) {
  size_t sz = vec.size();
  vec.resize(n);
  for (size_t i = sz; i < n; i++) {
    vec[i] = i;
  }
}
```

and Carruth's recommendation:

1. Allocation
2. Assignment

The difference between resize and reserve is that reserve allocates memory, but
resize initializes it.

The key difference that we discovered, is that resize adjusts the _size_ of the
vector, where reserve does not. So

```c++
vec.size() == n / 10; // true
vec.resize(n);
vec.size() == n;       // true
```

while

```c++
vec.size() == n / 10; // true
vec.reserve(n);
vec.size() == n / 10; // still true
```

So

```c++
vec.size() == n / 10;       // true
vec.reserve(n);
vec.push_back(10);
vec.size() == (n / 10) + 1;  // true
```

However, you cannot:

```c++
void append(size_t n, std::vector &vec) {
  size_t sz = vec.size();
  vec.reserve(n);
  for (size_t i = sz; i < n; i++) {
    vec[i] = i;
  }
  vec.size() == n; // false
}
```

But obviously, allocation + initialization (`resize`) is slower than allocation
alone (`reserve`), right?

## Assignment

With some common sense, it's obvious that bracket notation is faster than
`push_back`: `push_back` has to increment the size, check that it's still less
than capacity, and if its not, reallocate (the reallocation solved by the
reserve, but still). The bracket notation directly accesses the underlying
memory and just puts it in there.

## Putting the two together

The only way that resize + [] is faster than reserve + push_back is if the
combined overhead of push_back overwhelms the initialization of resize, right?
This is probably the case for some large n, but not for some small n I'd assume,
since memory reallocation is expensive (you have to allocate a new block of
memory and copy the whole array to the new block!).

Except, that's not true.

`resize()` initializes to zero unless you specify a value. And here's the thing
about zero-initialization: you can use [calloc][calloc]:

> For large allocations, most calloc implementations under mainstream OSes will
> get known-zeroed pages from the OS (e.g. via POSIX mmap(MAP_ANONYMOUS) or
> Windows VirtualAlloc) so it doesn't need to write them in user-space. This is
> how normal malloc gets more pages from the OS as well; calloc just takes
> advantage of the OS's guarantee.

That means zero-allocation is equivalent (or near equivalent) to uninitialized
allocation. So you get the initialization for free, `malloc == calloc`. Now the
only difference between the two patterns is `push_back`'s overhead, which is
obviously greater than bracket notation.

## tl;dr

Use

```c++
void append(size_t n, std::vector &vec) {
  size_t sz = vec.size();
  vec.resize(n);
  for (size_t i = sz; i < n; i++) {
    vec[i] = i;
  }
}
```

not

```c++
void append(size_t n, std::vector &vec) {
  size_t sz = vec.size();
  vec.reserve(n);
  for (size_t i = sz; i < n; i++) {
    vec.push_back(i);
  }
}
```

My boss was right, as usual.

[2014]: https://www.youtube.com/watch?v=fHNmRkzxHWs&t=2001s
[carbon]: https://github.com/carbon-language/carbon-lang
[2015]: https://www.youtube.com/watch?v=FnGCDLhaxKU
[calloc]: https://stackoverflow.com/a/1538427/9691276
