#!/usr/bin/env python3
"""Extract sequences from database for species in multiple hit file

Usage:
    <program> multiple_hit_file database_file
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
    def __repr__(self):
        return self.name + "\n" + self.sequence[:31] + "\n"

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
    multiple_hit_file = sys.argv[1]
    database_file = sys.argv[2]
except:
    print(__doc__)
    sys.exit(1)

# Read multiple hits file to extract species groups
multiple_hit_species_groups = [x.strip().split(",")[1].split(";")
        for x in open(multiple_hit_file).readlines()]

# Extract reads from database
all_species = set([species for sublist in multiple_hit_species_groups for species in sublist])
sequences_by_species_group = defaultdict(list)
sequences = fasta_iterator(database_file)

# Extract only species in the multiple hit species groups
for s in sequences:
    if s.name in all_species:
        sequences_by_species_group[s.name].append(s)

# Write sequence file for each multiple hit species group
for group in multiple_hit_species_groups:
    first_species = group[0]
    output_filname = first_species + "_multiple_hits.fasta"

    with open(output_filname, "w") as outfile:
        for species in sorted(group):
            for sequence in sequences_by_species_group[species]:
                sequence.write_to_file(outfile)

# Extract all species from genera in multiple hit species groups
all_genera = set(["_".join(x.split("_")[:2]) for x in all_species])
sequences_by_genus = defaultdict(list)
sequences = fasta_iterator(database_file)

for s in sequences:
    genus = "_".join(s.name.split("_")[:2])
    if genus in all_genera:
        sequences_by_genus[genus].append(s)

# Write sequence file for each multiple hit genera
for group in multiple_hit_species_groups:
    first_species = group[0]
    output_filname = first_species + "_whole_genus_multiple_hits.fasta"

    with open(output_filname, "w") as outfile:
        for species in sorted(group):
            genus = "_".join(species.split("_")[:2])
            for sequence in sequences_by_genus[genus]:
                sequence.write_to_file(outfile)

