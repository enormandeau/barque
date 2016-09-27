#!/bin/bash

# Parallel version
ls -1 03_trimmed/ | perl -pe 's/R[12].*\.fastq.gz//' | sort -u | parallel flash -t 1 -z -O -m 30 -M 280 03_trimmed/{}R1_001.fastq.gz 03_trimmed/{}R2_001.fastq.gz --to-stdout \> 04_merged/{}merged.fastq.gz

## Merge not parallel
#for i in $(ls -1 03_trimmed/ | perl -pe 's/R[12].*\.fastq.gz//' | sort -u)
#do
#    echo "Merging: $i"
#    flash -t 1 -z -O -m 30 -M 280 03_trimmed/"$i"R1_001.fastq.gz 03_trimmed/"$i"R2_001.fastq.gz > /dev/null
#    mv out.extendedFrags.fastq.gz 04_merged/"$i"merged.fastq.gz
#done

## Cleanup
#rm out.*

