#!/usr/bin/env python
"""Rename OTUs with shorter names (eg: otu00000001;size=13442;)

Usage:
    <program> input_fasta output_fasta
"""

# Modules
import sys

# Parse user input
try:
    input_fasta = sys.argv[1]
    output_fasta = sys.argv[2]
except:
    print(__doc__)
    sys.exit(1)

# Treat fasta file
otu_number = 1
with open(input_fasta) as infile:
    with open(output_fasta, "w") as outfile:
        for line in infile:
            if line.startswith(">"):
                name = ">otu_" + str(otu_number) + "_found_" + line.strip().split(";")[-1].split("=")[1] + "_times\n"
                otu_number += 1
                outfile.write(name)
            else:
                outfile.write(line)
