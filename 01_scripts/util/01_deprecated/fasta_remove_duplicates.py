#!/usr/bin/env python
"""Keep only unique sequences, regardless of sequence name

USAGE:
    <program> input_file output_file

Where:
    input_file is a .fasta or .fasta.gz file
    output_file is a .fasta or .fasta.gz file
"""

# Importing modules
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

# Parse user input
try:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
except:
    print(__doc__)
    sys.exit(1)

# Set of seen sequences
seen_sequences = set()

# Iterate through sequences and write to files
with myopen(output_file, "wt") as outf:
    for s in fasta_iterator(input_file):
        if not s.sequence in seen_sequences:
            seen_sequences.add(s.sequence)
            s.write_to_file(outf)
