#!/usr/bin/env python
"""Create BARQUE-compatible database from annotated OTUs

Usage:
    <program> vsearch_output otu_fasta output_database primer_file amplicon
"""

# Modules
from collections import defaultdict
from copy import deepcopy
import sys

# Parse user input
try:
    vsearch_output = sys.argv[1]
    otu_fasta = sys.argv[2]
    output_database = sys.argv[3]
    primer_file = sys.argv[4]
    amplicon = sys.argv[5]
except:
    print(__doc__)
    sys.exit(1)

# Read primer_file
primers = dict()
with open(primer_file) as pfile:
    for line in pfile:
        if line.startswith("#"):
            continue

        l = line.strip().split(",")
        primer = l[0]
        if primer == amplicon:
            species_threshold = float(l[6])
            genus_threshold = float(l[7])
            phylum_threshold = float(l[8])

# Get infos from vsearch_output
otu_dict = defaultdict(list)

with open(vsearch_output) as vfile:
    for line in vfile:
        l = line.split()
        otu = l[0]
        taxon = l[1]
        similarity = float(l[2])
        hit_length = int(l[3])
        otu_dict[otu].append([similarity, hit_length, taxon])

# Keep only best hit
for otu in otu_dict:
    infos = deepcopy(otu_dict[otu])
    best_similarity = infos[0][0]
    infos = [x for x in infos if x[0] >= best_similarity]

    # Decide on best annotation

    # Species
    if best_similarity >= species_threshold:
        species_list = list(set([x[2] for x in infos]))
        if len(species_list) == 1:
            otu_dict[otu] = species_list[0]
            continue

    # Species
    if best_similarity >= genus_threshold:
        genus_list = list(set(["_".join(x[2].split("_")[:2]) + "_unknown" for x in infos]))
        if len(genus_list) == 1:
            otu_dict[otu] = genus_list[0]
            continue

    # Species
    if best_similarity >= phylum_threshold:
        phylum_list = list(set(["_".join(x[2].split("_")[:1]) + "_unknown_unknown" for x in infos]))
        if len(phylum_list) == 1:
            otu_dict[otu] = phylum_list[0]
            continue

    # Otherwise, we cannot know anything about that taxon
    otu_dict[otu] = "unknown_unknown_unknown"

# Treat fasta file
with open(otu_fasta) as infile:
    with open(output_database, "w") as outfile:
        for line in infile:
            if line.startswith(">"):
                otu = line.strip()[1:]
                otu_list = otu.split("_")
                otu_num = otu_list[1]
                otu_size = otu_list[3]
                otu_name = "-".join(["otu", otu_num, otu_size])
                taxon = otu_dict[otu]

                if not taxon:
                    taxon = "unknown_unknown_unknown"

                outfile.write(">" + taxon + "-" + otu_name + "\n")

            else:
                outfile.write(line)
