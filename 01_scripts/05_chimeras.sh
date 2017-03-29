#!/bin/bash
# Find and remove chimeras

# Global variables
CHIMERASFOLDER="08_chimeras"

# Remove duplicated sequences
ls -1 "$CHIMERASFOLDER"/*.fasta |
    parallel vsearch --derep_fulllength {} --output {}.unique --sizeout

# Use regrouped amplicons to find chimeras with uchime
ls -1 "$CHIMERASFOLDER"/*.fasta.unique |
    parallel vsearch --uchime_denovo {} --chimeras {}.chimeras \
        --nonchimeras {}.nonchimeras --borderline {}.borderline
