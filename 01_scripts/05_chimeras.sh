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

# Remove them from single samples

# Remove them from regrouped amplicons
