#!/bin/bash
# Use completed BARQUE run to create one annotated OTU database per primer pair

# Global variables
CONFIG_FILE=$1
INFO_FOLDER="02_info"
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

    # Concatenate non-chimera data
    echo "BARQUE: Concatenating all non-chimera"
    cat 08_chimeras/*"$amplicon"_nonchimeras.fasta.gz > "$name".fasta.gz

    # Dereplicate
    echo "BARQUE: Dereplicating reads"
    vsearch --threads "$NCPUS" --derep_fulllength "$name".fasta.gz \
        --strand plus --output "$name".derep \
        --sizein --sizeout --fasta_width 0 \
        --minuniquesize 2 --minseqlength 20

    # Remove concatenated non-chimera data
    rm "$name".fasta.gz

    # Remove sequences with Ns
    echo "BARQUE: Removing sequences containing Ns"
    ./01_scripts/util/fasta_remove_sequences_with_N.py "$name".derep "$name".derep.no_Ns
    rm "$name".derep

    # Create OTUs
    echo "BARQUE: Creating OTUs"
    swarm -t "$NCPUS" -d 1 -f -l "$name".log \
        -o "$name".clusters \
        -s "$name".stats \
        -w "$name".otus.fasta -z \
        "$name".derep.no_Ns

    # Remove cluster file
    rm "$name".clusters

    # Rename sequences (name format: >otu_6_found_2315_times)
    echo "BARQUE: Renaming OTU sequences"
    ./01_scripts/util/rename_OTUs.py "$name".otus.fasta "$name".otus.renamed.fasta

    echo "####"
    echo
done

# Blast OTUs using databases
echo "BARQUE: Blasting OTUs"
./01_scripts/util/vsearch_OTUs.sh "$MAX_ACCEPTS" "$MAX_REJECTS" "$QUERY_COV" "$NCPUS"

# Create OTUs database
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
ls -1 "$OTU_FOLDER" | parallel -j "$NCPUS" gzip "$OTU_FOLDER"/{}
