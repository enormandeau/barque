#!/usr/bin/env python3
"""Format db_teleo1.fasta provided by Laetitia

Usage:
    <program> input_db output_db

Name format:
    >KX148472 family_name=Zoarcidae; species_name=Lycodes tanakae; family=8193; taxid=1358735; genus_name=Lycodes; rank=species; genus=8196; species=1358735;     Lycodes tanakae mitochondrion, complete genome
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

    def __repr__(self):
        return self.name + " " + self.sequence[:31]

# Functions
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

                name = line[1:]
                sequence = ""
                begun = True

            else:
                sequence += line

        if name != "":
            yield Fasta(name, sequence)

def myopen(_file, mode="rt"):
    if _file.endswith(".gz"):
        return gzip.open(_file, mode=mode)

    else:
        return open(_file, mode=mode)

# Parse user input
try:
    input_db = sys.argv[1]
    output_db = sys.argv[2]
except:
    print(__doc__)
    sys.exit(1)

# Process db
sequences = fasta_iterator(input_db)

with myopen(output_db, "wt") as outfile:
    for s in sequences:
        l = s.name.strip().split(";")
        family_name = l[0].split("=")[1]
        species_name = l[1].split("=")[1].split(".")[0]
        taxon = family_name + "_" + species_name.replace(" ", "_")
        taxon = taxon.replace("###", "unknown_unknown")
        s.name = taxon
        s.write_to_file(outfile)
