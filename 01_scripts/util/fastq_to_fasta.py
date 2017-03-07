#!/usr/bin/env python
"""Convert fastq to fasta

Usage:
    python fastq_to_fasta.py inputFile outputFile

Where:
    inputFile is a .fastq or a .fastq.gz file
    outputFile is a .fasta or a .fasta.gz file
"""

# Modules
import gzip
import sys

# Defining classes
class Fastq(object):
    """Fastq object with name and sequence
    """

    def __init__(self, name, seq, name2, qual):
        self.name = name[1:].replace(" ", ";")
        self.seq = seq
        self.name2 = name2
        self.qual = qual
        self.length = len(seq)

    def write_fasta(self, handle):
        handle.write(">" + self.name + ";" + "size=" + str(self.length) + ";\n")
        handle.write(self.seq + "\n")

# Defining functions
def myopen(infile, mode="r"):
    if infile.endswith(".gz"):
        return gzip.open(infile, mode=mode)
    else:
        return open(infile, mode=mode)

def fastq_parser(infile):
    """Takes a fastq file infile and returns a fastq object iterator
    """
    
    with myopen(infile) as f:
        while True:
            name = f.readline().strip()
            if not name:
                break

            seq = f.readline().strip()
            name2 = f.readline().strip()
            qual = f.readline().strip()
            yield Fastq(name, seq, name2, qual)

# Parsing user input
try:
    infile = sys.argv[1]
    outfile = sys.argv[2]
except:
    print __doc__
    sys.exit(1)

# Create sequence iterator
sequences = fastq_parser(infile)

# Treating the sequences
with myopen(outfile, "w") as ofile:
    for s in sequences:
        s.write_fasta(ofile)
