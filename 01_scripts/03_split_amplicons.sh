#!/bin/bash

# Parameters
NCPUS=$1
# TODO Add primer file?

# Global variables
INFOFOLDER="02_info"
MERGEDFOLDER="06_merged"
SPLITFOLDER="07_split_amplicons"
RESULTFOLDER="12_results"

# Split amplicons in parallel
ls -1 -S "$MERGEDFOLDER"/*.fastq.gz |
    parallel -j "$NCPUS" ./01_scripts/util/split_amplicons_one_file.py "$MERGEDFOLDER"/{/} \
    "$INFOFOLDER"/primers.csv \
    "$INFOFOLDER"/iupac.csv \
    "$SPLITFOLDER"

# Create summary in results folder
paste "$SPLITFOLDER"/*_summary.csv | perl -pe 's/\t[^,]+,/,/g' > "$RESULTFOLDER"/amplicon_split_summary.csv
