#!/bin/bash
# Netlify runs this (see netlify.toml). skyblue is written in c′, so build
# the compiler first; it bootstraps from C, so only cc and make are needed.
set -euo pipefail
git submodule update --init
make -C cprime
make -C skyblue
./skyblue/skyblue -i src -o build
