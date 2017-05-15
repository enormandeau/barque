#!/bin/bash
# Run test on small dataset
# NOTE: Works only on the developper's computer

CONFIGFILE=$1

# Cleanup temporary data and result directories
rm 04_data/*
./01_scripts/util/cleanup_analyses.sh

# Import small dataset, database, and primers
cp /home/labolb/temp.backup/barque_test_dataset/*.fastq.gz 04_data
cp /home/labolb/temp.backup/barque_test_dataset/bold.fasta.gz 03_databases/bold.fasta.gz
cp 02_info/primers.csv 02_info/primers.csv.bak_$(date +%Y-%m-%d_%H-%M-%S)
cp /home/labolb/temp.backup/barque_test_dataset/primers.csv 02_info

## Run all
./barque "$CONFIGFILE"
