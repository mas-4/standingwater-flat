---
title: "NanoDiffract test platform"
url: ""
featureImage: ""
short: "nanodiffract"
category: "platform"
ai: ""
order: "01"
year: "2021 – now"
tags: ["python", "pytest", "c", "c++", "postgresql", "azure devops", "rhel", "qt"]
---
My day job, since 2021: build and test engineering for NanoDiffract, Onto
Innovation's decades-old, 2M+ line C++ optical metrology software, in a
Windows shop. The work is finding the pain points in how the software gets
built and tested, and engineering them away.

- **The regression-testing system**, designed and built over five years. It's
  a pytest-based tool that generates reference results for each build, stores
  them in PostgreSQL, and runs PR validation and post-merge regressions on the
  compute cluster. Every NanoDiffract engineer relies on it.
- **A desktop GUI for it** (PySide6, Cythonized), now in use at five leading
  chipmakers and rolling out to every Onto customer.
- **Tooling on top of it**: automated bisection across official builds that
  finds the build behind a result change in minutes, where it used to be a
  manual, build-by-build hunt; a benchmark harness with statistical
  significance testing; and a memory monitor, a small HTTP server in C on each
  cluster node that the head node polls for memory use.
- **The cluster itself**: automated recovery of wedged and lost nodes for the
  application developers, and once, two weeks of tracking erratic behavior on
  80 nodes down to a faulty port on the server rack.
- **The build infrastructure**: I provision and maintain the build machines,
  write the teams' Azure DevOps pipelines, led compiler and dependency
  upgrades and a build-system redesign, and cleared about 7,000 compiler
  warnings by hand.
- **A Python C extension** reimplementing the software's neural net inference,
  so the ML engineers could analyze the results.

The code isn't public, so there's nothing to link to here.
