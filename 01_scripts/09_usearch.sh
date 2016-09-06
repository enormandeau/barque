#!/bin/bash

# Find best hit in COI database using usearch
for i in 06_amplicons_regrouped/all_coi*.fasta; do echo $i; usearch -usearch_local $i -db 99_databases/coi_db.udb -id 0.9 -maxaccepts 10 -maxrejects 100 -strand both -blast6out 07_blast_results/$(basename $i.coi_db) -top_hit_only -query_cov 0.5; done
