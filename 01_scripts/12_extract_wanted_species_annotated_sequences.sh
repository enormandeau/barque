#!/bin/bash
# Extract all the sequences that annotated to a specific species by sample and globally

# Global variables
SPECIES=$1
MIN_SIMILARITY=$2

# Test that global variable are set
if [[ -z $SPECIES || -z $MIN_SIMILARITY ]]
then
    echo "Usage: <program> species_name minimum_similarity"
    exit
fi

# Create a 14_SPECIES_sequences result folder (13 is reserved for OTUs)
OUTPUT_FOLDER=14_"$SPECIES"_sequences
mkdir "$OUTPUT_FOLDER" 2>/dev/null
rm "$OUTPUT_FOLDER"/*.ids 2>/dev/null
rm "$OUTPUT_FOLDER"/*.fasta 2>/dev/null

echo "Searching for: $SPECIES"

# Get names of sequences by sample
ls -1 09_vsearch/*.fasta.gz_unique.fasta.gz.*.gz |
    grep -v _matched\.fasta\.gz |
    parallel ./01_scripts/util/extract_sequence_names_for_species.py {} "$SPECIES" "$MIN_SIMILARITY" "$OUTPUT_FOLDER"

# Get the sequences by sample
ls -1 "$OUTPUT_FOLDER"/*_wanted.ids |
    while read i
    do
        STUB=$(basename "$i" | perl -pe 's/_wanted\.ids//')
        SEQUENCE_FILE=08_chimeras/"$STUB"_nonchimeras.fasta.gz_unique.fasta.gz
        01_scripts/util/fasta_extract.py "$SEQUENCE_FILE" "$i" "$OUTPUT_FOLDER"/"$STUB".fasta
    done

# Put all the sequences together
cat "$OUTPUT_FOLDER"/*.fasta > "$OUTPUT_FOLDER"/.temp_sequences

# Keep only unique sequences
./01_scripts/util/combine_unique_sequences.py "$OUTPUT_FOLDER"/.temp_sequences 999999999 "$OUTPUT_FOLDER"/"$SPECIES"_all_sites_combined_wanted.fasta

# Cleanup
rm "$OUTPUT_FOLDER"/.temp_sequences
rm "$OUTPUT_FOLDER"/*_wanted.ids
