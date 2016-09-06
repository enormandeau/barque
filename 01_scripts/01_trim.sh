#!/bin/bash

ls -1 02_data/*.fastq.gz | perl -pe 's/R[12].*gz//' | sort -u |
    parallel -k -j 16 ./01_scripts/trimmomatic.sh {}

rm trimmomatic.log
