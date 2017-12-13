#!/bin/bash
# Trim reads and remove
# - Reads with bad quality
# - Short reads

# Parameters
NCPUS=$1
MIN_HIT_LENGTH=$2
CROP_LENGTH=$3

# Global variables
DATA_FOLDER="04_data"

# Parallelize on all raw data files
ls -1 -S "$DATA_FOLDER"/*_R1_*.fastq.gz |
    perl -pe 's/R[12].*gz//' |
    parallel -k -j "$NCPUS" ./01_scripts/util/trimmomatic.sh {} "$MIN_HIT_LENGTH" "$CROP_LENGTH"
