#!/bin/bash
# Use completed BARQUE run to create one annotated OTU database per primer pair

# Global variables
CONFIG_FILE=$1
INFO_FOLDER="02_info"
AMPLICON_FOLDER="07_split_amplicons"
OTU_FOLDER="13_otu_database"

# Import configfile
if [ -s "$CONFIG_FILE" ]
then
    source "$CONFIG_FILE"
else
    echo -e "\nBARQUE: Config file does not exist or is empty."
    echo -e "        Please specify a valid config file."
    exit 1
fi

# Create empty working folder
rm -rf "$OTU_FOLDER"/* 2>/dev/null
mkdir "$OTU_FOLDER" 2>/dev/null

for amplicon in $(grep -v "^#" "$INFO_FOLDER"/primers.csv | awk -F "," '{print $1}')
do
    name="$OTU_FOLDER"/"$amplicon"
    echo
    echo "####"
    echo "BARQUE: Creating OTUs for $amplicon"

    # Concatenate 07_split_amplicons/*_merged_"$amplicon".fastq.gz
    echo "BARQUE: Concatenating all amplicon files"
    cat "$AMPLICON_FOLDER"/*_merged_"$amplicon".fastq.gz > "$name".fastq.gz

    # Transform to fasta.gz
    echo "BARQUE: Transforming to fasta file"
    ./01_scripts/util/fastq_to_fasta.py "$name".fastq.gz "$name".fasta.gz
    rm "$name".fastq.gz

    # Dereplicate
    echo "BARQUE: Dereplicating reads"
    vsearch --threads "$NCPUS" --derep_fulllength "$name".fasta.gz \
        --strand plus --output "$name".derep \
        --sizeout --fasta_width 0 \
        --minuniquesize 2

    # Find chimeras with uchime
    echo "BARQUE: Finding chimeras"
    vsearch --uchime_denovo "$name".derep \
        --chimeras "$name".chimeras \
        --nonchimeras "$name".nonchimeras \
        --borderline "$name".borderline \
        --mindiff 2 \
        --mindiv 0.4 \
        --minh 0.2 \
        --minuniquesize "$MIN_SIZE_FOR_OTU" \
        --relabel OTU_ \
        --sizeout \
        --fasta_width 0

    # Remove sequences with Ns
    echo "BARQUE: Removing sequences containing Ns"
    ./01_scripts/util/fasta_remove_sequences_with_N.py "$name".nonchimeras "$name".nonchimeras_no_Ns

    # Remove singletons or rare reads
    echo "BARQUE: Dereplicating reads"
    vsearch --threads "$NCPUS" --derep_fulllength "$name".nonchimeras_no_Ns \
        --strand plus --output "$name".nonchimeras_no_Ns_above_"$MIN_SIZE_FOR_OTU" \
        --sizein --sizeout --fasta_width 0 \
        --minuniquesize "$MIN_SIZE_FOR_OTU"

    # Create OTUs:
    echo "BARQUE: Creating OTUs"
    vsearch --cluster_smallmem "$name".nonchimeras_no_Ns_above_"$MIN_SIZE_FOR_OTU" \
        --threads "$NCPUS" \
        --id 0.97 \
        --sizein \
        --usersort \
        --relabel OTU_ \
        --centroids "$name".centroids \
        --clusterout_sort \
        --consout "$name".concensus \
        --sizeorder \
        --sizeout

    # Rename sequences (name format: >otu_6_found_2315_times)
    echo "BARQUE: Renaming OTU sequences"
    ./01_scripts/util/rename_OTUs.py "$name".centroids "$name".otus.renamed.fasta

    echo "####"
    echo
done

# Blast OTUs using databases
echo "BARQUE: Blasting OTUs"
./01_scripts/util/vsearch_OTUs.sh "$MAX_ACCEPTS" "$MAX_REJECTS" "$QUERY_COV" "$NCPUS"

# Create OTUs database
echo "BARQUE: Creating OTU databases"
for amplicon in $(grep -v "^#" "$INFO_FOLDER"/primers.csv | awk -F "," '{print $1}')
do
    name="$OTU_FOLDER"/"$amplicon"

    ./01_scripts/util/create_OTU_database.py \
        "$name".otus.vsearch.fasta \
        "$name".otus.renamed.fasta \
        "$name".otus.database.fasta \
        "$PRIMER_FILE" \
        "$amplicon"
done

# Cleanup (compress all files in $OTU_FOLDER)
echo "BARQUE: Cleaning up"
ls -1 "$OTU_FOLDER" | parallel -j "$NCPUS" gzip "$OTU_FOLDER"/{}
