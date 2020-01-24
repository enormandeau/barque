#!/bin/bash

# Parameters
MAX_ACCEPTS=$1
MAX_REJECTS=$2
QUERY_COV=$3
NCPUS=$4

# Global variables
INFO_FOLDER="02_info"
OTU_FOLDER="13_otu_database"

# Find best hit in database using vsearch
for amplicon in $(grep -v "^#" "$INFO_FOLDER"/primers.csv | awk -F "," '{print $1}')
do
    echo "Blasting $amplicon"
    name="$OTU_FOLDER"/"$amplicon"
    database=$(grep -v "^#" "$INFO_FOLDER"/primers.csv | grep "$amplicon" | awk -F "," '{print $6}').fasta.gz
    min_similarity=$(grep -v "^#" "$INFO_FOLDER"/primers.csv | grep "$amplicon" | awk -F "," '{print $9}')

    echo
    echo "#############################"
    echo "# Using database: $database"
    echo "#############################"
    echo

    # Run vsearch
    vsearch_input="$name".otus.renamed.fasta
    vsearch_result="$name".otus.vsearch.fasta
    vsearch_matched="$name".otus.vsearch.matched.fasta
    echo "Running vsearch on $name.otus.renamed.gz with database $database"
    vsearch --usearch_global "$vsearch_input" -db 03_databases/"$database" \
        --threads "$NCPUS" --qmask none --dbmask none --id "$min_similarity" \
        --blast6out "$vsearch_result" \
        --dbmatched "$vsearch_matched" \
        --maxaccepts "$MAX_ACCEPTS" --maxrejects "$MAX_REJECTS" --maxhits "$MAX_ACCEPTS" \
        --query_cov "$QUERY_COV" --fasta_width 0 --minseqlength 20
        echo "done"
        echo "--"
    echo
done
