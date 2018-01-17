#!/bin/bash

# Parameters
MAX_ACCEPTS=$1
MAX_REJECTS=$2
QUERY_COV=$3
NCPUS=$4

# Global variables
INFO_FOLDER="02_info"
CHIMERA_FOLDER="08_chimeras"
VSEARCH_FOLDER="09_vsearch"

# Find best hit in database using vsearch
for amplicon in $(grep -v "^#" "$INFO_FOLDER"/primers.csv | awk -F "," '{print $1}')
do
    echo "Amplicon: $amplicon"
    database=$(grep -v "^#" "$INFO_FOLDER"/primers.csv | grep "$amplicon" | awk -F "," '{print $6}').fasta.gz
    min_similarity=$(grep -v "^#" "$INFO_FOLDER"/primers.csv | grep "$amplicon" | awk -F "," '{print $9}')

    echo
    echo "#############################"
    echo "# Using database: $database"
    echo "#############################"
    echo

    # Treat each sample
    for sample in $(ls -1 "$CHIMERA_FOLDER"/*"$amplicon"*_nonchimeras.fasta.gz)
    do
        # File names
        vsearch_fasta=$(basename "$sample")
        fasta="${vsearch_fasta%_nonchimeras.fasta}"_unique.fasta.gz

        # Create fasta file
        ./01_scripts/util/fasta_format_non_chimera.py \
            "$CHIMERA_FOLDER"/"$vsearch_fasta" "$CHIMERA_FOLDER"/"$fasta"

        # Run vsearch
        echo
        echo "Running vsearch on $fasta with database $database"
        vsearch --usearch_global "$CHIMERA_FOLDER"/"$fasta" -db 03_databases/"$database" \
            --threads "$NCPUS" --qmask none --dbmask none --id "$min_similarity" \
            --blast6out "$VSEARCH_FOLDER"/"${fasta%.fasta}"."${database%.fasta.gz}" \
            --dbmatched "$VSEARCH_FOLDER"/"${fasta%.fasta}"."${database%.fasta.gz}_matched.fasta" \
            --maxaccepts "$MAX_ACCEPTS" --maxrejects "$MAX_REJECTS" --maxhits "$MAX_ACCEPTS" \
            --query_cov "$QUERY_COV" --fasta_width 0
        echo "done"
        echo "--"
        echo
    done
done

# Cleanup
ls -1 -S "$VSEARCH_FOLDER"/* | grep -v "\.gz$" | parallel -j "$NCPUS" gzip --force {}
