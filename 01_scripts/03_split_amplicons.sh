#!/bin/bash

# Parameters
NCPUS=$1
# TODO Add primer file?

# Global variables
INFO_FOLDER="02_info"
MERGED_FOLDER="06_merged"
SPLIT_FOLDER="07_split_amplicons"
RESULT_FOLDER="12_results"

# Split amplicons in parallel
ls -1 -S "$MERGED_FOLDER"/*.fastq.gz |
    parallel -j "$NCPUS" ./01_scripts/util/split_amplicons_one_file.py "$MERGED_FOLDER"/{/} \
    "$INFO_FOLDER"/primers.csv \
    "$INFO_FOLDER"/iupac.csv \
    "$SPLIT_FOLDER"

# Create summary in results folder
paste "$SPLIT_FOLDER"/*_summary.csv | perl -pe 's/\t[^,]+,/,/g' > "$RESULT_FOLDER"/amplicon_split_summary.csv
