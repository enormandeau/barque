#!/bin/bash
# Find and remove chimeras

# Global variables
NCPUS=$1
INFO_FOLDER="02_info"
SPLIT_FOLDER="07_split_amplicons"
CHIMERA_FOLDER="08_chimeras"

# Remove file with all chimeras
rm "$CHIMERA_FOLDER"/all.chimeras 2>/dev/null

# Remove duplicated sequences
ls -1 -S "$CHIMERA_FOLDER"/*.fasta |
    parallel vsearch --derep_fulllength {} --output {}.unique --sizeout --fasta_width 0

# Use regrouped amplicons to find chimeras with uchime
ls -1 -S "$CHIMERA_FOLDER"/*.fasta.unique |
    parallel vsearch --uchime_denovo {} --chimeras {}.chimeras \
        --nonchimeras {}.nonchimeras --borderline {}.borderline --fasta_width 0

# Concatenate all chimera and borderline seqneces found
cat "$CHIMERA_FOLDER"/*.chimeras "$CHIMERA_FOLDER"/*.borderline > "$CHIMERA_FOLDER"/all.chimeras

# Remove chimera and borderline sequences from split amplicon sequences
for amplicon in $(grep -v "^#" "$INFO_FOLDER"/primers.csv | awk -F "," '{print $1}')
do
    # Remove chimera sequences from split folder
    echo "Removing chimeras from: $amplicon"
    ls -1 -S "$SPLIT_FOLDER"/*"$amplicon"*.fastq.gz | parallel -j "$NCPUS" \
        ./01_scripts/util/remove_chimeras.py {} "$CHIMERA_FOLDER"/all.chimeras "$CHIMERA_FOLDER"/{/}
done

# Cleanup
ls -1 -S "$CHIMERA_FOLDER"/chimera_* | parallel -j "$NCPUS" gzip {}

# Report results
gunzip -c "$CHIMERA_FOLDER"/chimera_*.chimeras.gz > 12_results/chimera_sequences.fasta
