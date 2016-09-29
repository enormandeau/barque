#!/bin/bash
# Trim reads and remove
# - Reads with bad quality
# - Adapters
# - Short reads

# Global variables
BASE=$(basename $1)
TRIMMOMATIC_JAR=/home/labolb/Software/trinity_pipeline_ibis/00_archive/trimmomatic-0.30.jar
ADAPTERFILE=00_archive/primers_henrik.fasta

# Trimmomatic
java -XX:ParallelGCThreads=1 -cp $TRIMMOMATIC_JAR org.usadellab.trimmomatic.TrimmomaticPE \
    -phred33 \
    02_data/"$BASE"R1_001.fastq.gz \
    02_data/"$BASE"R2_001.fastq.gz \
    03_trimmed/"$BASE"R1_001.fastq.gz \
    03_trimmed/"$BASE"R1_001.single.fastq.gz \
    03_trimmed/"$BASE"R2_001.fastq.gz \
    03_trimmed/"$BASE"R2_001.single.fastq.gz \
    ILLUMINACLIP:"$ADAPTERFILE":3:30:6 \
    LEADING:20 \
    TRAILING:20 \
    SLIDINGWINDOW:20:20 \
    MINLEN:200 2>/dev/null

## Cleanup
rm 03_trimmed/"$BASE"R1_001.single.fastq.gz 2>/dev/null
rm 03_trimmed/"$BASE"R2_001.single.fastq.gz 2>/dev/null
