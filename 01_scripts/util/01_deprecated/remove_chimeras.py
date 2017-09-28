#!/usr/bin/env python
"""Remove chimera sequences identified by vsearch from split amplicons

Usage:
    ./01_scripts/util/remove_chimeras.py inputFastq unwantedFasta outputFastq
"""

# Modules
import gzip
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

class Fastq(object):
    """Fastq object with name and sequence
    """
    def __init__(self, name, seq, name2, qual):
        self.name = name
        self.seq = seq
        self.name2 = name2
        self.qual = qual
    def write_to_file(self, handle):
        handle.write("@" + self.name + "\n")
        handle.write(self.seq + "\n")
        handle.write("+" + self.name2 + "\n")
        handle.write(self.qual + "\n")
    def write_fasta(self, handle):
        handle.write(">" + self.name + "\n")
        handle.write(self.seq + "\n")

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

def fastq_parser(input_file):
    """Takes a fastq file infile and returns a fastq object iterator
    """
    with myopen(input_file) as f:
        while True:
            name = f.readline().strip()[1:]
            if not name:
                break
            seq = f.readline().strip()
            name2 = f.readline().strip()[1:]
            qual = f.readline().strip()
            yield Fastq(name, seq, name2, qual)


# Parse user input
try:
    inputFastq = sys.argv[1]
    unwantedFasta = sys.argv[2]
    outputFastq = sys.argv[3]
except:
    print __doc__
    sys.exit(1)

# Read unwantedFasta
unwanted = set()
fasta_sequences = fasta_iterator(unwantedFasta)
for seq in fasta_sequences:
    unwanted.add(seq.sequence)

# Filter sequences
fastq_sequences = fastq_parser(inputFastq)

with myopen(outputFastq, "wt") as outfile:
    for seq in fastq_sequences:
        if not seq.seq in unwanted:
            seq.write_to_file(outfile)
