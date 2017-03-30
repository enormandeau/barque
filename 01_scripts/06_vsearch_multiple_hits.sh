#!/bin/bash

# Parameters
SIMILARITY_RESULTS=$1
SIMILARITY_VSEARCH=$2
MAX_ACCEPTS=$3
MAX_REJECTS=$4
QUERY_COV=$5
NCPUS=$6

# Global variables
INFOFOLDER="02_info"
CHIMERAFOLDER="08_chimeras"
VSEARCHFOLDER="09_vsearch_multiple_hits"

# Find best hit in database using vsearch
for amplicon in $(grep -v "^#" "$INFOFOLDER"/primers.csv | awk -F "," '{print $1}')
do
    database=$(grep -v "^#" "$INFOFOLDER"/primers.csv | grep $amplicon | awk -F "," '{print $6}').fasta
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

        # Run vsearch
        echo "Running vsearch on $fasta with database $database"
        #vsearch -vsearch_local "$CHIMERAFOLDER"/"$fasta" -db 03_databases/"$database" -id "$SIMILARITY_RESULTS" \
        #    -maxaccepts "$MAX_ACCEPTS" -maxrejects "$MAX_REJECTS" -strand both -blast6out \
        #    "$VSEARCHFOLDER"/"${fasta%.fasta}"."${database%.udb}" -top_hits_only -query_cov "$QUERY_COV"
        vsearch --usearch_global "$CHIMERAFOLDER"/"$fasta" -db 03_databases/"$database" \
            --threads "$NCPUS" --qmask none --dbmask none --id "$SIMILARITY_VSEARCH" \
            --blast6out "$VSEARCHFOLDER"/"${fasta%.fasta}"."${database%.fasta}" \
            --dbmatched "$VSEARCHFOLDER"/"${fasta%.fasta}"."${database%.fasta}_matched.fasta" \
            --maxaccepts "$MAX_ACCEPTS" --maxrejects "$MAX_REJECTS" --maxhits 10 \
            --query_cov "$QUERY_COV"

        # Cleanup fasta file
        rm "$CHIMERAFOLDER"/"$fasta"
    done
done
