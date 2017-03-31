#!/bin/bash
# Find and remove chimeras

# Global variables
NCPUS=$1
INFOFOLDER="02_info"
SPLITFOLDER="07_split_amplicons"
CHIMERASFOLDER="08_chimeras"

# Remove file with all chimeras
rm "$CHIMERASFOLDER"/all.chimeras 2>/dev/null

# Remove duplicated sequences
ls -1 "$CHIMERASFOLDER"/*.fasta |
    parallel vsearch --derep_fulllength {} --output {}.unique --sizeout

# Use regrouped amplicons to find chimeras with uchime
ls -1 "$CHIMERASFOLDER"/*.fasta.unique |
    parallel vsearch --uchime_denovo {} --chimeras {}.chimeras \
        --nonchimeras {}.nonchimeras --borderline {}.borderline

# Concatenate all chimera and borderline seqneces found
cat "$CHIMERASFOLDER"/*.chimeras "$CHIMERASFOLDER"/*.borderline > "$CHIMERASFOLDER"/all.chimeras

# Remove chimera and borderline sequences from split amplicon sequences
for amplicon in $(grep -v "^#" "$INFOFOLDER"/primers.csv | awk -F "," '{print $1}')
do
    # Remove chimera sequences from split folder
    echo "$amplicon"
    ls -1 "$SPLITFOLDER"/*"$amplicon"*.fastq.gz | parallel -j "$NCPUS" \
        ./01_scripts/util/remove_chimeras.py {} "$CHIMERASFOLDER"/all.chimeras "$CHIMERASFOLDER"/{/}

done

# Cleanup
ls -1 "$CHIMERASFOLDER"/chimera_* | parallel -j "$NCPUS" gzip {}
