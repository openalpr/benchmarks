#!/bin/bash

echo "Starting Benchmark..."
~/projects/alpr/src/build/misc_utilities/benchmark us segocr ./usimages/ ./ | grep ".png" |  sed 's/?//g' | sort > results.csv

echo "Total entries:"
diff -y ./results.csv ./groundtruth.csv | wc -l

echo ""
echo "Entries with differences"
diff -y ./results.csv ./groundtruth.csv | grep "|" | wc -l

echo ""
echo "Type this command to see diffs"
echo 'diff -y ./results.csv ./groundtruth.csv | grep "|"' 

# Save benchmark run to history
echo `date` : `diff -y ./results.csv ./groundtruth.csv | grep "|" | wc -l` errors >> ./history
