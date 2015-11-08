#! /usr/bin/env bash

# Copyright (c) 2014, 2015 Mario Mlačak, mmlacak@gmail.com
# See accompanying LICENSE.txt for details.


cd src

# rm -rf *.hi
# rm -rf *.o
# rm -rf crochess*

ghc -O3 -threaded Main.hs -o crochess

ls -Fal --color=auto

cd ..

