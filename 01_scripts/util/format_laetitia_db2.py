#!/usr/bin/env python3
"""Format db_teleo1.fasta provided by Laetitia

Usage:
    <program> input_db output_db

Name format:
    Info lines are semi-colon separated and contain (names are only examples):
        family_name=Zoarcidae;
        species_name=Lycodes tanakae;
        genus_name=Lycodes;
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
        handle.write(self.sequence.upper() + "\n")

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
        family_name = [x for x in l if "family_name" in x][0].split("=")[1]
        #genus_name = [x for x in l if "genus_name" in x][0].split("=")[1]
        species_name = [x for x in l if "species_name" in x][0].split("=")[1]
        species_name = "_".join(species_name.split(" ")[0: 2])

        taxon = "_".join([family_name, species_name])
        taxon = taxon.replace("###", "unknown")
        s.name = taxon
        s.write_to_file(outfile)
