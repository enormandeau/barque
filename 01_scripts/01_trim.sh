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

# Grab file name ending
# Parallelize on all raw data files
ENDING=$(ls -1 -S "$DATA_FOLDER"/*_R1*.fastq.gz |
    head -1 |
    grep -P "_R1(_001)?.fastq.gz" |
    perl -pe 's/.*_(R[12](_001)?\.fastq\.gz)/\1/')

if [ -z ENDING ]
then
    echo "Modify fastq.gz file format to fit documentation"
    exit 1
else
    echo "  File ending: $ENDING"
fi

# Parallelize on all raw data files
ls -1 -S "$DATA_FOLDER"/*_R1*.fastq.gz |
    grep -P "_R1(_001)?.fastq.gz" |
    perl -pe 's/_R[12](_001)?\.fastq\.gz/_/' |
    parallel -k -j "$NCPUS" ./01_scripts/util/trimmomatic.sh {} "$MIN_HIT_LENGTH" "$CROP_LENGTH" "$ENDING"
