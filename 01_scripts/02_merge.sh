#!/bin/bash

# Merge
for i in $(ls -1 03_trimmed/ | perl -pe 's/R[12].*\.fastq.gz//' | sort -u)
do
    echo "Merging: $i"
    flash -t 1 -z -O -m 30 -M 280 03_trimmed/"$i"R1_001.fastq.gz 03_trimmed/"$i"R2_001.fastq.gz > /dev/null
    mv out.extendedFrags.fastq.gz 04_merged/"$i"merged.fastq.gz
done

# Cleanup
rm out.*
