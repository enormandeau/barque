#!/usr/bin/env python3
"""Filter out fasta sequences containing Ns

Usage:
    <program> input_fasta output_fasta
"""

# Modules
import sys

# Classes
class Fasta(object):
    """Fasta object with name and sequence
    """

    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence

    def write_to_file(self, handle):
        handle.write(">" + self.name + "\n")
        handle.write(self.sequence + "\n")

    def __repr__(self):
        return self.name + "\t" + self.sequence[0:31]

# Function
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
    input_fasta = sys.argv[1]
    output_fasta = sys.argv[2]
except:
    print(__doc__)
    sys.exit(1)

# Filter sequences
sequences = fasta_iterator(input_fasta)

with open(output_fasta, "w") as outfile:
    for s in sequences:
        if not "N" in s.sequence.upper():
            s.write_to_file(outfile)
