#!/bin/bash
# From vsearch results, identify cases of multiple hits in order to create a
# list of species to remove from the database

for file in 09_vsearch/*
do
    for i in $(awk '{print $1}' $file | sort | uniq -c | sort -nr | head | awk '{print $2}')
    do
        grep $i $file | awk '{print $2}' | sort | uniq -c | sort -nr | awk '{print $2}'
        echo
    done
done | perl -pe 's/\n/_newline_/g' |
    perl -pe 's/_newline__newline_/\n/g' |
    grep _newline_ |
    sort |
    uniq -c |
    sort -nr |
    awk '{print $1,$2}' |
    perl -pe 's/ / time(s):\n/' |
    perl -pe 's/_newline_/\n/g' |
    perl -pe 's/^(\d)/\n\1/' > 12_results/multiple_hits.txt
