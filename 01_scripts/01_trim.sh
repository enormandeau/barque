#!/bin/bash
# Trim reads and remove
# - Reads with bad quality
# - Adapters
# - Short reads

# Global variables
DATAFOLDER="04_data"

ls -1 "$DATAFOLDER"/*.fastq.gz |
    perl -pe 's/R[12].*gz//' |
    sort -u |
    parallel -k -j 16 ./01_scripts/util/trimmomatic.sh {}
