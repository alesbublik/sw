#!/bin/bash

tail -n +2 $1 | sort -g --parallel=1 -k2 -k1 --field-separator=, > temp.txt
sw temp.txt
