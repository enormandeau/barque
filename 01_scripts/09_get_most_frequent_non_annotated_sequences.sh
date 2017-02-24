#!/bin/bash
# For each sample, eliminate the sequences with annotation found with usearch,
# find the 100 most frequent sequences and put them in a fasta file for further
# blasts on NCBI nr/nt.

# Get names of unwanted sequences from 11_usearch
echo "Finding unwanted sequences (these with usearch results)..."
ls -1 11_usearch/ | cut -d "_" -f 1 | sort -u | while read i
do
    cat 11_usearch/"$i"* |
        awk '{print $1}' |
        cut -d ";" -f 1 > 14_non_annotated_sequences/"$i"_unwanted.ids
done

# Remove these from 06 merged and output a fasta file per sample
echo "Removing these sequences from the merged sequences of each sample..."
for i in $(ls -1 14_non_annotated_sequences/ | grep \.ids$)
do
    input="${i%_unwanted.ids}"
    output="${i%_unwanted.ids}"_wanted.fasta.gz
    echo "  Treating: $input"
    ./01_scripts/util/fastq_remove.py 06_merged/"$input"*_merged.fastq.gz 14_non_annotated_sequences/"$i" 14_non_annotated_sequences/"$output"
done

# Get the 100 most frequent sequences and their count per sample
echo "Extracting the 100 most frequent sequences present more than 1000 times in each sample..."
for i in 14_non_annotated_sequences/*.fasta.gz
do
    echo "  Treating: ${i#14_non_annotated_sequences}"
    gunzip -c "$i" |
        grep -v "^>" |
        sort |
        uniq -c |
        sort -nr |
        awk '$1 > 1000 {print ">found_"$1"_times\n"$2}' |
        head -100 > "${i%.fasta.gz}"_most_present.fasta
done

# Get the 10 most represented sequences per sample
head -20 14_non_annotated_sequences/*_wanted_most_present.fasta |
    grep -v "^==" > most_present_non_annotated_sequences.fasta
