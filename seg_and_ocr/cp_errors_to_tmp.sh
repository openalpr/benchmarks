#!/bin/bash

mkdir /tmp/a
rm /tmp/a/*
diff -y ./results.csv ./groundtruth.csv | grep "|" | gawk '{print $1; }' | sed 's/,.*//g' | xargs -I {} cp ./usimages/{} /tmp/a/

echo "Error images copied to /tmp/a/"

echo "Run this command to troubleshoot:"
echo " ~/projects/alpr/src/build/misc_utilities/classifychars /tmp/a/ /tmp"
