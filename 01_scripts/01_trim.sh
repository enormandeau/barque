#!/bin/bash
# Trim reads and remove
# - Reads with bad quality
# - Short reads

# Parameters
NCPUS=$1

# Global variables
DATAFOLDER="04_data"

# Parallelize on all raw data files
ls -1 "$DATAFOLDER"/*.fastq.gz |
    perl -pe 's/R[12].*gz//' |
    sort -u |
    parallel -k -j "$NCPUS" ./01_scripts/util/trimmomatic.sh {}
