#!/bin/bash
# Find and remove chimeras

# Global variables
NCPUS=$1
SKIP_CHIMERA_DETECTION=$2
INFO_FOLDER="02_info"
SPLIT_FOLDER="07_split_amplicons"
CHIMERA_FOLDER="08_chimeras"
RESULT_FOLDER="12_results"

# Treat all database files
for amplicon in $(grep -v "^#" "$INFO_FOLDER"/primers.csv | awk -F "," '{print $1}')
do
    echo "Amplicon: $amplicon"

    # fastq_to_fasta
    ls -1 -S "$SPLIT_FOLDER"/*_merged_"$amplicon".fastq.gz |
    parallel -j "$NCPUS" ./01_scripts/util/fastq_to_fasta.py {} "$CHIMERA_FOLDER"/{/.}.fasta

done

# Remove duplicated sequences
ls -1 -S "$CHIMERA_FOLDER"/*.fasta |
parallel -j "$NCPUS" vsearch --derep_fulllength {} --output {}.unique --sizeout --fasta_width 0

if [ "$SKIP_CHIMERA_DETECTION" == "0" ]
then
    echo -e "\nBARQUE: Looking for chimeras"

    # Find chimeras with uchime
    ls -1 -S "$CHIMERA_FOLDER"/*.fasta.unique |
    parallel -j "$NCPUS" vsearch --uchime_denovo {} --chimeras {}.chimeras \
        --nonchimeras {}.nonchimeras --borderline {}.borderline --fasta_width 0

    # Report results
    cat "$CHIMERA_FOLDER"/*.unique.chimeras > "$RESULT_FOLDER"/chimera_sequences.fasta

    # Cleanup
    ls -1 -S "$CHIMERA_FOLDER"/*.{fasta,unique,borderline,chimeras} 2>/dev/null | parallel -j "$NCPUS" gzip {}

    for i in "$CHIMERA_FOLDER"/*.nonchimeras
    do
        mv "$i" "${i%.fastq.fasta.unique.nonchimeras}"_nonchimeras.fasta
    done

elif [ "$SKIP_CHIMERA_DETECTION" == "1" ]
then
    echo -e "\nBARQUE: Skipping chimera detection"

    for i in "$CHIMERA_FOLDER"/*.unique
    do
        mv "$i" "${i%.fastq.fasta.unique}"_nonchimeras.fasta
    done

    ls -1 -S "$CHIMERA_FOLDER"/*.{fastq.fasta,fastq.fasta_unique.fasta} 2>/dev/null | parallel -j "$NCPUS" gzip {}

else
    echo -e "\nWARNING: Invalid value in config file for SKIP_CHIMERA_DETECTION"
fi
