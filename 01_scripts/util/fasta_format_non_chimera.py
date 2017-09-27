#!/usr/bin/env python
"""Convert vsearch unique fasta to barque unique fasta

Usage:
    python fasta_to_unique_fasta.py inputFile outputFile

Where:
    inputFile is a .fasta or a .fasta.gz file from vsearch
    outputFile is a .fasta or a .fasta.gz file in barque unique format
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

# Treating the sequences
with myopen(outfile, "wt") as outfile:
    seq_num = 1
    for s in sequences:
        count = s.name.split("=")[-1].replace(";", "")
        s.name = "sequence_" + str(seq_num) + "_found_" + count + "_times"
        seq_num += 1
        s.write_to_file(outfile)
