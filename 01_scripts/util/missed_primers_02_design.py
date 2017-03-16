#!/usr/bin/env python
"""Design degenerate primers from a file with one sequence per line

Note: The sequences must not be degenerate and have the same length

Usage:
    ./01_scripts/util/missed_primers_02_design.py input_file
"""

# Modules
import sys

# Get user input
try:
    input_file = sys.argv[1]
except:
    print(__doc__)
    sys.exit(1)

# Functions

# Iupac characters
iupac = {
        "A": "A",
        "C": "C",
        "G": "G",
        "T": "T",
        "AG": "R",
        "CT": "Y",
        "CG": "S",
        "AT": "W",
        "GT": "K",
        "AC": "M",
        "CGT": "B",
        "AGT": "D",
        "ACT": "H",
        "ACG": "V",
        "ACGT": "N",
        }

# Read all sequences in a list
sequences = []
with open(input_file) as infile:
    for line in infile:
        seq = line.strip()
        sequences.append(seq)

# Find possible nucleotides at each position
degenerate = []
for i in xrange(len(sequences[0])):
    nucleotides = "".join(sorted(list(set([x[i] for x in sequences]))))
    degenerate.append(nucleotides)

# Create and print degenerate primer
primer = []
for n in degenerate:
    primer.append(iupac[n])

print("".join(primer))
