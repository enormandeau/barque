#!/usr/bin/env python
"""Combine most frequent sequences into unique sequences while keeping an
accurate count information with each sequence.

Usage:
    ./01_scripts/util/combine_unique_sequences.py input_fasta num_sequences output_fasta

Note:
    the sequence names in input_fasta must have the following format:

    >sequence_466_found_676_times
    >sequence_392_found_377_times
    >sequence_45_found_373_times
    >sequence_11_found_184_times
    >sequence_74_found_115_times
    >sequence_343_found_74_times
    >sequence_25_found_30_times
    >sequence_476_found_23_times
    >sequence_319_found_17_times
    >sequence_57_found_14_times
"""

# Importing modules
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
    input_fasta = sys.argv[1]
    num_sequences = int(sys.argv[2])
    output_fasta = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Count sequences
fasta_sequences = fasta_iterator(input_fasta)
fasta_dict = defaultdict(int)

for s in fasta_sequences:
    num = int(s.name.split("_")[3])
    fasta_dict[s.sequence] += num

sequence_counts = sorted([(x[1], x[0]) for x in fasta_dict.items()], reverse=True)
counter = 1

with open(output_fasta, "w") as outfile:
    for seq in sequence_counts[:num_sequences]:
        name = "sequence_" + str(counter) + "_found_" + str(seq[0]) + "_times"
        sequence = seq[1]
        s = Fasta(name, sequence)
        s.write_to_file(outfile)
        counter += 1
