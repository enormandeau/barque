#!/bin/bash
# Remove any result and temporary file from folders 05_trimmed and up

# Cleanup temporary data and result directories
rm 05_trimmed/* 06_merged/* 07_split_amplicons/* 08_chimeras/* 09_vsearch/* \
    10_read_dropout/* 12_results/* 11_non_annotated/* \
    most_frequent_non_annotated_sequences.fasta multiple_hits.txt 2>/dev/null
