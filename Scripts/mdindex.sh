#!/bin/bash

while read fname; 
do
    title=$(head -1 docs/$f | sed 's/^# //')
    echo "- [$title]($fname)"
done < $1
