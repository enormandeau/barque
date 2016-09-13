#!/bin/bash

# Compile databases if needed
#ls -1 99_databases/*.fasta | parallel usearch -makeudb_usearch {} -output {.}.udb

# Find best hit in COI database using usearch
for amplicon in $(grep -v "^#" primers.csv | awk '{print $1}')
do
    database=$(grep -v "^#" primers.csv | grep $amplicon primers.csv | awk '{print $5}').udb
    echo "#######################"
    echo "# database: $database"
    echo "#######################"

    # Treat each sample
    for sample in $(ls -1 05_split_by_amplicon/*"$amplicon"*.fastq.gz)
    do
        # File names
        fastq=$(basename "$sample")
        fasta="${fastq%.fastq.gz}".fasta

        # Create fasta file
        echo
        ./01_scripts/util/fastq_to_fasta.py 05_split_by_amplicon/"$fastq" 05_split_by_amplicon/"$fasta"

        ## -dirty-hack- # (keep only top sequences)
        #head -2000 05_split_by_amplicon/"$fasta" > 05_split_by_amplicon/"$fasta".temp
        #mv 05_split_by_amplicon/"$fasta".temp 05_split_by_amplicon/"$fasta"

        # Run usearch
        echo "Running usearch on $fasta with database $database"

        # usearch local (fast, best in our case)
        usearch -usearch_local 05_split_by_amplicon/"$fasta" -db 99_databases/"$database" -id 0.9 \
            -maxaccepts 10 -maxrejects 100 -strand both -blast6out \
            07_blast_results/"${fasta%.fasta}"."${database%.udb}" -top_hit_only -query_cov 0.5

        # Cleanup fasta file
        rm 05_split_by_amplicon/"$fasta"
    done
done
