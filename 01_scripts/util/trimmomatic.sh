#!/bin/bash
# Trim reads and remove
# - Reads with bad quality
# - Adapters
# - Short reads

# Global variables
BASE=$(basename $1)
TRIMMOMATIC_JAR=/home/labolb/Software/trinity_pipeline_ibis/00_archive/trimmomatic-0.30.jar
ADAPTERFILE="02_info/illumina_adapters.fas"
DATAFOLDER="04_data"
TRIMMEDFOLDER="05_trimmed"

# Trimmomatic
java -XX:ParallelGCThreads=1 -cp $TRIMMOMATIC_JAR org.usadellab.trimmomatic.TrimmomaticPE \
    -phred33 \
    "$DATAFOLDER"/"$BASE"R1_001.fastq.gz \
    "$DATAFOLDER"/"$BASE"R2_001.fastq.gz \
    "$TRIMMEDFOLDER"/"$BASE"R1_001.fastq.gz \
    "$TRIMMEDFOLDER"/"$BASE"R1_001.single.fastq.gz \
    "$TRIMMEDFOLDER"/"$BASE"R2_001.fastq.gz \
    "$TRIMMEDFOLDER"/"$BASE"R2_001.single.fastq.gz \
    LEADING:20 \
    TRAILING:20 \
    SLIDINGWINDOW:20:20 \
    MINLEN:100

## Cleanup
rm "$TRIMMEDFOLDER"/"$BASE"R1_001.single.fastq.gz 2>/dev/null
rm "$TRIMMEDFOLDER"/"$BASE"R2_001.single.fastq.gz 2>/dev/null
