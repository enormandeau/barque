#!/bin/bash
# Regroup all samples per amplicon

for amplicon in $(awk '{print $1}' primers.csv)
do
    echo "Treating: $amplicon"
    REGROUPED=06_amplicons_regrouped/all_"$amplicon".fastq

    # Create empty fastq file
    rm "$REGROUPED" 2>/dev/null
    touch "$REGROUPED"

    # Concatenate all samples
    for i in $(ls -1 05_split_by_amplicon | grep "$amplicon")
    do
        gunzip -c 05_split_by_amplicon/"$i" >> "$REGROUPED"
    done

    # fastq_to_fasta
    fastq_to_fasta.py "$REGROUPED" "${REGROUPED%.fastq}".fasta

    # Cleanup
    rm "$REGROUPED" 2>/dev/null
done
