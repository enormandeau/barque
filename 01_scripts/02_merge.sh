#!/bin/bash

TRIMMEDFOLDER="05_trimmed"
MERGEDFOLDER="06_merged"

# Parallel version
ls -1 "$TRIMMEDFOLDER"/ | perl -pe 's/R[12].*\.fastq.gz//' | sort -u | parallel flash -t 1 -z -O -m 30 -M 280 "$TRIMMEDFOLDER"/{}R1_001.fastq.gz "$TRIMMEDFOLDER"/{}R2_001.fastq.gz --to-stdout \> "$MERGEDFOLDER"/{}merged.fastq.gz

## Merge not parallel
#for i in $(ls -1 "$TRIMMEDFOLDER"/ | perl -pe 's/R[12].*\.fastq.gz//' | sort -u)
#do
#    echo "Merging: $i"
#    flash -t 1 -z -O -m 30 -M 280 "$TRIMMEDFOLDER"/"$i"R1_001.fastq.gz "$TRIMMEDFOLDER"/"$i"R2_001.fastq.gz > /dev/null
#    mv out.extendedFrags.fastq.gz "$MERGEDFOLDER"/"$i"merged.fastq.gz
#done

## Cleanup
#rm out.*

