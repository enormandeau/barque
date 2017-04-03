#!/bin/bash
# Remove any result and temporary file from folders 05_trimmed and up

# Cleanup temporary data and result directories
rm 05_trimmed/* 06_merged/* 07_split_amplicons/* 08_chimeras/* 09_vsearch_multiple_hits/* 10_summary_multiple_hits/* 11_vsearch/* 12_summary/* 13_read_dropout/* 14_non_annotated_sequences/* 15_results/* most_frequent_non_annotated_sequences.fasta multiple_hits.txt 2>/dev/null
