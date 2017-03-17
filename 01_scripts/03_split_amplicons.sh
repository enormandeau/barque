#!/bin/bash

# Parameters
NCPUS=$1
# TODO Add primer file?

# Global variables
INFOFOLDER="02_info"
MERGEDFOLDER="06_merged"
SPLITFOLDER="07_split_amplicons"

# Split amplicons in parallel
ls -1 "$MERGEDFOLDER"/*.fastq.gz |
    parallel -j "$NCPUS" ./01_scripts/util/split_amplicons_one_file.py "$MERGEDFOLDER"/{/} \
    "$INFOFOLDER"/primers.csv \
    "$INFOFOLDER"/iupac.csv \
    "$SPLITFOLDER"
