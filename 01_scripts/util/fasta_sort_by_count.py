#!/usr/bin/env python
"""Sort fasta sequences produced by Barque with most frequen sequences first

USAGE:
    python ./01_scripts/util/fasta_sort_by_count.py input_file output_file

Where:
    input_file is a .fasta or .fasta.gz file
    output_file is a .fasta or .fasta.gz file
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
    def __repr__(self):
        return self.name + "\t" + self.sequence[0:31]

# Defining functions
def myopen(infile, mode="r"):
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
        yield Fasta(name, sequence)

# Parse user input
try:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
except:
    print __doc__
    sys.exit(1)

# Iterate through sequences and get count info
fasta_sequences = fasta_iterator(input_file)
counts = defaultdict(list)

for seq in fasta_sequences:
    count = int(seq.name.split("_")[3])
    counts[count].append(seq)

with myopen(output_file, "w") as outf:
    for c in sorted(counts, reverse=True):
        for s in counts[c]:
            s.write_to_file(outf)
