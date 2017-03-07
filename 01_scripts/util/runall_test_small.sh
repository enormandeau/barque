#!/bin/bash

# Cleanup temporary data and result directories
rm 04_data/* 05_trimmed/* 06_merged/* 07_split_amplicons/* 08_chimeras/* 09_usearch_multiple_hits/* 10_results_multiple_hits/* 11_usearch/* 12_results/* 13_read_dropout/* most_present_non_annotated_sequences.fasta multiple_hits.txt 2>/dev/null

# Import small dataset
cp /home/labolb/temp.backup/barque_test_dataset/*.gz 04_data

# Run all
./01_scripts/util/runall.sh
