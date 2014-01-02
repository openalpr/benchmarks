#!/bin/bash

~/projects/alpr/src/build/misc_utilities/benchmark us speed ./usimages/ ./ | tee results.txt

echo "Results copied to results.txt"
