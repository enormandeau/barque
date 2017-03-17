#!/bin/bash

# Parameters
NCPUS=$1
MIN_OVERLAP=$2
MAX_OVERLAP=$3

# Global variables
TRIMMEDFOLDER="05_trimmed"
MERGEDFOLDER="06_merged"

# Parallelize on all trimmed files
ls -1 "$TRIMMEDFOLDER"/ |
    perl -pe 's/R[12].*\.fastq.gz//' |
    sort -u |
    parallel -j "$NCPUS" flash -t 1 -z -O -m "$MIN_OVERLAP" -M "$MAX_OVERLAP" \
        "$TRIMMEDFOLDER"/{}R1_001.fastq.gz "$TRIMMEDFOLDER"/{}R2_001.fastq.gz \
        --to-stdout \> "$MERGEDFOLDER"/{}merged.fastq.gz
