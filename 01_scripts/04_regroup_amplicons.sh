#!/bin/bash
# Regroup all samples per amplicon

# Global variables
INFOFOLDER="02_info"
SPLITFOLDER="07_split_amplicons"
CHIMERAFOLDER="08_chimeras"

# Regroup all samples per amplicon
for amplicon in $(grep -v "^#" "$INFOFOLDER"/primers.csv | awk -F "," '{print $1}')
do
    echo "Treating: $amplicon"
    REGROUPED="$CHIMERAFOLDER"/all_"$amplicon".fastq

    # Create empty fastq file
    rm "$REGROUPED" 2>/dev/null
    touch "$REGROUPED"

    # Concatenate all samples
    for i in $(ls -1 "$SPLITFOLDER" | grep "$amplicon")
    do
        gunzip -c "$SPLITFOLDER"/"$i" >> "$REGROUPED"
    done

    # fastq_to_fasta
    ./01_scripts/util/fastq_to_fasta.py "$REGROUPED" "${REGROUPED%.fastq}".fasta.gz

    # Cleanup
    rm "$REGROUPED" 2>/dev/null
done
