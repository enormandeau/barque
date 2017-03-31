#!/bin/bash
# Run test on small dataset
# NOTE: Works only on the developper's computer

CONFIGFILE=$1

# Cleanup temporary data and result directories
rm 04_data/* 05_trimmed/* 06_merged/* 07_split_amplicons/* 08_chimeras/* 09_vsearch_multiple_hits/* 10_summary_multiple_hits/* 11_vsearch/* 12_summary/* 13_read_dropout/* 14_non_annotated_sequences/* 15_results/* most_frequent_non_annotated_sequences.fasta multiple_hits.txt 2>/dev/null

# Import small dataset, database, and primers
cp /home/labolb/temp.backup/barque_test_dataset/*.fastq.gz 04_data
cp /home/labolb/temp.backup/barque_test_dataset/bold.fasta.gz 03_databases
cp 02_info/primers.csv 02_info/primers.csv.bak_$(date +%Y-%m-%d_%H-%M-%S)
cp /home/labolb/temp.backup/barque_test_dataset/primers.csv 02_info

## Run all
./barque "$CONFIGFILE"
