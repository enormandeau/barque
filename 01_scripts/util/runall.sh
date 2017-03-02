#!/bin/bash
# Script to test the full pipeline

# Format bold datase (and place in proper folder)
# TODO

# Trim and clean reads
echo "Trimming and filtering reads"
./01_scripts/01_trim.sh

# Merge forward and reverse reads
echo "Merging forward and reverse reads"
./01_scripts/02_merge.sh

# Split samples by amplicon
echo "Splitting samples by amplicon"
./01_scripts/03_split_amplicons.sh

# Regroup amplicons to look for chimeras
echo "Regrouping amplicons"
echo "...Skipping for now"
#./01_scripts/04_regroup_amplicons.sh

# Look for chimeras
echo "Looking for chimeras"
echo "...Skipping for now"
#./01_scripts/05_chimeras.sh

## Run usearch for multiple hits
#echo "Running usearch with multiple hits"
#./01_scripts/06_usearch_multiple_hits.sh

## Summarize results for multiple hits
#echo "Summarizing results with multiple hits"
#./01_scripts/07_summarize_results.py 09_usearch_multiple_hits/ 10_results_multiple_hits/ 02_info/primers.csv 96 130 1

# Run usearch
echo "Running usearch"
./01_scripts/06_usearch.sh

# Summarize results
echo "Summarizing results"
./01_scripts/07_summarize_results.py 11_usearch/ 12_results/ 02_info/primers.csv 96 130 1

# Looking at sequence dropout
./01_scripts/08_summarize_read_dropout.sh

# Finding most frequent non-annotated sequences
./01_scripts/09_get_most_frequent_non_annotated_sequences.sh
