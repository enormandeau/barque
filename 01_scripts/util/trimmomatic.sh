#!/bin/bash
# Trim reads and remove
# - Reads with bad quality
# - Short reads

# Global variables
BASE=$(basename $1)
MIN_HIT_LENGTH=$2
CROP_LENGTH=$3
TRIMMOMATIC_JAR="01_scripts/util/trimmomatic-0.36.jar"
ADAPTERFILE="02_info/illumina_adapters.fas"
DATA_FOLDER="04_data"
TRIMMED_FOLDER="05_trimmed"

# Trimmomatic
java -XX:ParallelGCThreads=1 -cp "$TRIMMOMATIC_JAR" org.usadellab.trimmomatic.TrimmomaticPE \
    -phred33 \
    "$DATA_FOLDER"/"$BASE"R1_001.fastq.gz \
    "$DATA_FOLDER"/"$BASE"R2_001.fastq.gz \
    "$TRIMMED_FOLDER"/"$BASE"R1_001.fastq.gz \
    "$TRIMMED_FOLDER"/"$BASE"R1_001.single.fastq.gz \
    "$TRIMMED_FOLDER"/"$BASE"R2_001.fastq.gz \
    "$TRIMMED_FOLDER"/"$BASE"R2_001.single.fastq.gz \
    LEADING:20 \
    TRAILING:20 \
    SLIDINGWINDOW:20:20 \
    MINLEN:"$MIN_HIT_LENGTH" \
    CROP:"$CROP_LENGTH"

## Cleanup
rm "$TRIMMED_FOLDER"/"$BASE"R1_001.single.fastq.gz 2>/dev/null
rm "$TRIMMED_FOLDER"/"$BASE"R2_001.single.fastq.gz 2>/dev/null
