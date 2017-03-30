#!/bin/bash

# Parameters
SIMILARITY_RESULTS=$1
SIMILARITY_USEARCH=$2
MAXACCEPTS=$3
MAXREJECTS=$4
QUERYCOV=$5

# Global variables
INFOFOLDER="02_info"
CHIMERAFOLDER="08_chimeras"
USEARCHFOLDER="09_usearch_multiple_hits"

# Find best hit in database using usearch
for amplicon in $(grep -v "^#" "$INFOFOLDER"/primers.csv | awk -F "," '{print $1}')
do
    database=$(grep -v "^#" "$INFOFOLDER"/primers.csv | grep $amplicon | awk -F "," '{print $6}').udb
    echo "#######################"
    echo "# database: $database"
    echo "#######################"

    # Treat each sample
    for sample in $(ls -1 "$CHIMERAFOLDER"/*"$amplicon"*.fastq.gz)
    do
        # File names
        fastq=$(basename "$sample")
        fasta="${fastq%.fastq.gz}"_unique_multihits.fasta

        # Create fasta file
        echo
        ./01_scripts/util/fastq_to_unique_fasta.py "$CHIMERAFOLDER"/"$fastq" "$CHIMERAFOLDER"/"$fasta"

        # Run usearch
        echo "Running usearch on $fasta with database $database"
        usearch -usearch_local "$CHIMERAFOLDER"/"$fasta" -db 03_databases/"$database" -id "$SIMILARITY_RESULTS" \
            -maxaccepts "$MAXACCEPTS" -maxrejects "$MAXREJECTS" -strand both -blast6out \
            "$USEARCHFOLDER"/"${fasta%.fasta}"."${database%.udb}" -top_hits_only -query_cov "$QUERYCOV"

        # Cleanup fasta file
        rm "$CHIMERAFOLDER"/"$fasta"
    done
done
