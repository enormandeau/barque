#!/bin/bash
# Remove any result and temporary file from folders 05_trimmed and up

# Cleanup temporary data and result directories
rm 05_trimmed/* 06_merged/* 07_split_amplicons/* 08_chimeras/* 09_usearch_multiple_hits/* 10_results_multiple_hits/* 11_usearch/* 12_results/* 13_read_dropout/* most_present_non_annotated_sequences.fasta multiple_hits.txt 2>/dev/null
