#!/bin/bash
# For each sample, eliminate the sequences with annotation found with vsearch,
# find the 100 most frequent sequences and put them in a fasta file for further
# blasts on NCBI nr/nt.

# Parameters
NUM_NON_ANNOTATED_SEQ=$1
NCPUS=$2
CHIMERA_FOLDER="08_chimeras"
RESULT_FOLDER="12_results"
NON_ANNOTATED_FOLDER="11_non_annotated"

# Get names of unwanted sequences from 09_vsearch
ls -1 09_vsearch/ | grep -v _matched\.fasta | cut -d "_" -f 1 | sort -u | while read i
do
    rm "$NON_ANNOTATED_FOLDER"/"$i"_with_result.ids 2> /dev/null

    for j in $(ls -1 09_vsearch/"$i"_* | grep -v "_matched\.fasta")
    do
        gunzip -c "$j" |
            awk '$3 >= 97 {print $1}' |
            cut -d ";" -f 1 |
            uniq >> "$NON_ANNOTATED_FOLDER"/"$i"_with_result.ids
    done

    # Sort them by decreasing order of count (most frequent sequences first)
    gunzip -c "$CHIMERA_FOLDER"/"$i"_*_unique.fasta.gz > "$NON_ANNOTATED_FOLDER"/"$i"_temp.fasta
    ./01_scripts/util/fasta_sort_by_count.py \
        "$NON_ANNOTATED_FOLDER"/"$i"_temp.fasta \
        "$NON_ANNOTATED_FOLDER"/"$i"_unique.fasta

    rm "$NON_ANNOTATED_FOLDER"/"$i"_temp.fasta
done

# Remove these from "$CHIMERA_FOLDER"/*.fasta and output a fasta file per sample
for i in "$NON_ANNOTATED_FOLDER"/*.ids
do
    idfile=$(basename "$i")
    input="${idfile%_with_result.ids}"
    ./01_scripts/util/fasta_remove.py \
        "$NON_ANNOTATED_FOLDER"/"$input"_unique.fasta \
        "$NON_ANNOTATED_FOLDER"/"$input"_with_result.ids \
        "$NON_ANNOTATED_FOLDER"/"$input"_without_result.fasta
done

# Get the top most represented unique sequences per sample
cat "$NON_ANNOTATED_FOLDER"/*_without_result.fasta > "$RESULT_FOLDER"/most_frequent_non_annotated_sequences.temp

# Recombine identical sequence
./01_scripts/util/combine_unique_sequences.py "$RESULT_FOLDER"/most_frequent_non_annotated_sequences.temp "$NUM_NON_ANNOTATED_SEQ" "$RESULT_FOLDER"/most_frequent_non_annotated_sequences.fasta

# Cleanup
rm "$RESULT_FOLDER"/most_frequent_non_annotated_sequences.temp
ls -1 -S "$NON_ANNOTATED_FOLDER"/*.fasta | grep -v "\.gz$" | parallel -j "$NCPUS" gzip --force {}
