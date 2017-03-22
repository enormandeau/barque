#!/bin/bash
# Find and remove chimeras

# Global variables
CHIMERASFOLDER="08_chimeras"

# Remove duplicated sequences
ls -1 "$CHIMERASFOLDER"/*.fasta |
    parallel ./01_scripts/util/fasta_remove_duplicates.py {} {}.unique

# Use regrouped amplicons to find chimeras with uchime
ls -1 "$CHIMERASFOLDER"/*.fasta.unique |
    parallel usearch -uchime_denovo {} -uchimeout {}.uchime -chimeras {}.chimeras \
    -uchimealns {}.alignments \>\& {.}.uchime.message.small

# Copy results in 12_results
cp "$CHIMERASFOLDER"/*.fasta.unique.chimeras 12_results

# Cleanup
#rm 08_chimeras/*.fasta
#rm 08_chimeras/*.fasta.unique
