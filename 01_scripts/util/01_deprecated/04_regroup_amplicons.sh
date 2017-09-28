#!/bin/bash
# Regroup all samples per amplicon

# Global variables
INFO_FOLDER="02_info"
SPLIT_FOLDER="07_split_amplicons"
CHIMERA_FOLDER="08_chimeras"

# Regroup all samples per amplicon
for amplicon in $(grep -v "^#" "$INFO_FOLDER"/primers.csv | awk -F "," '{print $1}')
do
    echo "Regrouping: $amplicon"
    REGROUPED="$CHIMERA_FOLDER"/chimera_"$amplicon".fastq

    # Create empty fastq file
    rm "$REGROUPED" 2>/dev/null
    touch "$REGROUPED"

    # Concatenate all samples
    for i in $(ls -1 "$SPLIT_FOLDER" | grep merged_"$amplicon"\.fastq.gz)
    do
        gunzip -c "$SPLIT_FOLDER"/"$i" >> "$REGROUPED"
    done

    # fastq_to_fasta
    ./01_scripts/util/fastq_to_fasta.py "$REGROUPED" "${REGROUPED%.fastq}".fasta

    # Cleanup
    rm "$REGROUPED" 2>/dev/null
done
