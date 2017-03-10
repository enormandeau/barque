#!/bin/bash
# Run test on small dataset
# NOTE: Works only on the developper's computer

# Cleanup temporary data and result directories
rm 04_data/* 05_trimmed/* 06_merged/* 07_split_amplicons/* 08_chimeras/* 09_usearch_multiple_hits/* 10_results_multiple_hits/* 11_usearch/* 12_results/* 13_read_dropout/* most_present_non_annotated_sequences.fasta multiple_hits.txt 2>/dev/null 14_non_annotated_sequences/*

# Import small dataset, database, and primers
cp /home/labolb/temp.backup/barque_test_dataset/*.gz 04_data
cp /home/labolb/temp.backup/barque_test_dataset/bold.udb 03_databases
cp 02_info/primers.csv 02_info/primers.csv.bak_$(date +%Y-%m-%d_%H-%M-%S)
cp /home/labolb/temp.backup/barque_test_dataset/primers.csv 02_info

## Run all
time ./01_scripts/util/runall.sh
