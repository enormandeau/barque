#!/bin/bash
# Find and remove chimeras

# Remove duplicated sequences
ls -1 06_amplicons_regrouped/*.fasta | parallel ./01_scripts/util/fasta_remove_duplicates.py {} {}.unique

# Use regrouped amplicons to find chimeras with uchime
ls -1 06_amplicons_regrouped/*.fasta.unique | parallel usearch -uchime_denovo {} -uchimeout {.}.uchime \>\& {.}.uchime.message.small

# Remove them from single samples

# Remove them from regrouped amplicons
