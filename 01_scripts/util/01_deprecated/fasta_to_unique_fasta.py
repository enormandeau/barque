#!/usr/bin/env python
"""Convert fasta to fasta keeping only one unique representant of each read

Usage:
    python fasta_to_unique_fasta.py inputFile outputFile

Where:
    inputFile is a .fasta or a .fasta.gz file
    outputFile is a .fasta or a .fasta.gz file
"""

# Modules
from collections import defaultdict
import gzip
import sys

# Defining classes
class Fasta(object):
    """Fasta object with name and sequence
    """
    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence
    def write_to_file(self, handle):
        handle.write(">" + self.name + "\n")
        handle.write(self.sequence + "\n")

# Defining functions
def myopen(infile, mode="rt"):
    if infile.endswith(".gz"):
        return gzip.open(infile, mode=mode)
    else:
        return open(infile, mode=mode)

def fasta_iterator(input_file):
    """Takes a fasta file input_file and returns a fasta iterator
    """
    with myopen(input_file) as f:
        sequence = ""
        name = ""
        begun = False
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if begun:
                    yield Fasta(name, sequence)
                name = line.replace(">", "")
                sequence = ""
                begun = True
            else:
                sequence += line

        if name != "":
            yield Fasta(name, sequence)

# Parsing user input
try:
    infile = sys.argv[1]
    outfile = sys.argv[2]
except:
    print(__doc__)
    sys.exit(1)

# Create sequence iterator
sequences = fasta_iterator(infile)

# Find unique sequences
unique_sequences = defaultdict(int)
for s in sequences:
    unique_sequences[s.sequence] += 1

# Treating the sequences
with myopen(outfile, "wt") as outfile:
    seq_count = 0
    for s in unique_sequences:
        seq_count += 1
        name = ">sequence_" + str(seq_count) + "_found_" + str(unique_sequences[s]) + "_times"
        fasta_seq = Fasta(name, s)
        fasta_seq.write_to_file(outfile)
