#!/bin/bash

# Global variables
INFOFOLDER="02_info"
SPLITFOLDER="07_split_amplicons"
USEARCHFOLDER="09_usearch_multiple_hits"

# Find best hit in database using usearch
for amplicon in $(grep -v "^#" "$INFOFOLDER"/primers.csv | awk '{print $1}')
do
    database=$(grep -v "^#" "$INFOFOLDER"/primers.csv | grep $amplicon | awk '{print $5}').udb
    echo "#######################"
    echo "# database: $database"
    echo "#######################"

    # Treat each sample
    for sample in $(ls -1 "$SPLITFOLDER"/*"$amplicon"*.fastq.gz)
    do
        # File names
        fastq=$(basename "$sample")
        fasta="${fastq%.fastq.gz}"_usearch_multihits.fasta

        # Create fasta file
        echo
        ./01_scripts/util/fastq_to_unique_fasta.py "$SPLITFOLDER"/"$fastq" "$SPLITFOLDER"/"$fasta"

        # Run usearch
        echo "Running usearch on $fasta with database $database"

        # usearch local (fast, best in our case)
        usearch -usearch_local "$SPLITFOLDER"/"$fasta" -db 03_databases/"$database" -id 0.96 \
            -maxaccepts 10 -maxrejects 50 -strand both -blast6out \
            "$USEARCHFOLDER"/"${fasta%.fasta}"."${database%.udb}" -top_hits_only -query_cov 0.5

        # Cleanup fasta file
        rm "$SPLITFOLDER"/"$fasta"
    done
done
