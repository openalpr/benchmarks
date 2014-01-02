#!/bin/bash

~/projects/alpr/src/build/misc_utilities/benchmark us endtoend ./usimages/ ./

echo "Total entries:"
diff -y ./results.txt ./groundtruth.txt | wc -l

echo ""
echo "Entries with differences"
diff -y ./results.txt ./groundtruth.txt | grep "|" | wc -l

echo ""
echo "Type this command to see diffs"
echo 'diff -y ./results.txt ./groundtruth.txt | grep "|"' 

