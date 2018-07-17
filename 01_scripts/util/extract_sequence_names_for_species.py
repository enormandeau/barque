#!/usr/bin/env python3
"""Get sequence names of sequences that have a best hit on a specific species

Usage:
    <program> input_file wanted_species min_similarity output_folder

Where:
    input_file is the name of the vsearch output
    wanted_species is the full species name as found in the vsearch output
        eg: Fish_Salvelinus_alpinus
    min_similarity is the minimum percentage of similarity for the first hit
    output_folder is the name of the folder where the sequences will be put
"""

# Modules
import gzip
import sys
import os
import re

# Defining functions
def myopen(infile, mode="rt"):
    if infile.endswith(".gz"):
        return gzip.open(infile, mode=mode)
    else:
        return open(infile, mode=mode)

# Parse user input
try:
    input_file = sys.argv[1]
    wanted_species = sys.argv[2]
    min_similarity = float(sys.argv[3])
    output_folder = sys.argv[4]
except:
    print(__doc__)
    sys.exit()

sequences_treaded = set()
output_file_stub = re.sub("_nonchimeras\.fasta\.gz_unique\.fasta\.gz.*\.gz", "", os.path.basename(input_file))

with open(os.path.join(output_folder,
     output_file_stub + "_wanted.ids"),
    "w") as outfile:

    with myopen(input_file) as infile:

        for line in infile:
            l = line.strip().split()
            seq_name = l[0]
            species = l[1]
            similarity = l[2]

            if seq_name not in sequences_treaded:
                sequences_treaded.add(seq_name)

                if species == wanted_species and float(similarity) >= min_similarity:
                    outfile.write(seq_name + "\n")
