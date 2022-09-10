#!/bin/bash
[ ! -d "/path/to/dir" ] && mkdir bluesky/build
cd bluesky/build
cmake ..
cmake --build .
cd ../../
./bluesky/build/bluesky -vfi src -o build
