#!/bin/bash
# For each sample, eliminate the sequences with annotation found with usearch,
# find the 100 most frequent sequences and put them in a fasta file for further
# blasts on NCBI nr/nt.

# Parameters
NUM_NON_ANNOTATED_SEQ=$1

# Get names of unwanted sequences from 11_usearch
echo "Finding unwanted sequences (these with usearch results)..."
ls -1 11_usearch/ | cut -d "_" -f 1 | sort -u | while read i
do
    cat 11_usearch/"$i"_* |
        awk '{print $1}' |
        cut -d ";" -f 1 > 14_non_annotated_sequences/"$i"_with_result.ids

    # Sort them by decreasing order of count (most frequent sequences first)
    cat 07_split_amplicons/"$i"_*_unique.fasta > 14_non_annotated_sequences/"$i"_temp.fasta
    ./01_scripts/util/fasta_sort_by_count.py \
        14_non_annotated_sequences/"$i"_temp.fasta \
        14_non_annotated_sequences/"$i"_unique.fasta
    rm 14_non_annotated_sequences/"$i"_temp.fasta
done

# Remove these from 07_split_amplicons/*.fasta and output a fasta file per sample
echo "Removing these sequences from the merged sequences of each sample..."
for i in 14_non_annotated_sequences/*.ids
do
    idfile=$(basename "$i")
    input="${idfile%_with_result.ids}"
    output="${idfile%_with_result.ids}"_without_result.fasta.gz
    echo "  Treating: $input"
    ./01_scripts/util/fasta_remove.py 14_non_annotated_sequences/"$input"_unique.fasta 14_non_annotated_sequences/"$input"_with_result.ids 14_non_annotated_sequences/"$input"_without_result.fasta
done

# Get the 100 most represented unique sequences per sample
head -n $[ $NUM_NON_ANNOTATED_SEQ * 2 ] 14_non_annotated_sequences/*_without_result.fasta |
    grep -v "^==" |
    grep -vE "^$" > 12_results/most_frequent_non_annotated_sequences.fasta
