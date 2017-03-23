#!/usr/bin/env python
"""After blasting the most frequent non-annotated sequences and blasting them
on NCBI, use this script to report the number of non annotated sequences
for each species (or annotation) found on NCBI.

Usage:
    ./01_scripts/10_report_species_for_non_annotated_sequences.py AlignmentFile OutputFile

Where:
    AlignmentFile is the file downloaded from NCBI after the blast
    OutputFile is the name of the output file in .csv format
"""

# Modules
from collections import defaultdict
import sys

# Parsing user input
try:
    AlignmentFile = sys.argv[1]
    OutputFile = sys.argv[2]
except:
    print(__doc__)
    sys.exit(1)

# Prepare dictionary of species (or annotations)
species_dict = defaultdict(int)

# Read file
with open(AlignmentFile, "r+") as afile:
    lines = [x.strip() for x in afile.readlines()]

# Collect species and count information
line_num = 0
while line_num < len(lines):
    line = lines[line_num]
    if line.startswith("Query="):
        count = int(line.strip().split("_")[3])
        line_num += 1
        line = lines[line_num]
        while not line.startswith("Query="):
            line_num += 1
            line = lines[line_num]
            if line.startswith(">"):
                species = " ".join(line.split(" ")[1:3])
                species_dict[species] += count
                break

    line_num+=1

# Sort by decreasing number of sequences
species_infos = sorted([(x[1], x[0]) for x in species_dict.items()], reverse=True)

# Write output file
with open(OutputFile, "w") as ofile:
    ofile.write("Species,SequenceCount\n")
    for s in species_infos:
        ofile.write(s[1] + "," + str(s[0]) + "\n")
