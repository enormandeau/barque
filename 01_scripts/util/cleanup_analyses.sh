#!/bin/bash
# Remove any result and temporary file from folders 05_trimmed and up

# Cleanup temporary data and result directories
rm 05_trimmed/* 2>/dev/null
rm 06_merged/* 2>/dev/null
rm 07_split_amplicons/* 2>/dev/null
rm 08_chimeras/* 2>/dev/null
rm 09_vsearch/* 2>/dev/null
rm 10_read_dropout/* 2>/dev/null
rm 11_non_annotated/* 2>/dev/null
rm 12_results/* 2>/dev/null
rm 12_results/01_multihits/* 2>/dev/null
rm most_frequent_non_annotated_sequences.fasta 2>/dev/null
rm multiple_hits.txt 2>/dev/null
