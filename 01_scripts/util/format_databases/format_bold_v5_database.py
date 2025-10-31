#!/usr/bin/env python3
"""Prepare a fasta file from BOLD and prepare it for COI blast db

- Keep only 'Genus species' sequences

Usage:
    <program> input_fasta output_fasta

Where:
    input_fasta is a .fasta or a .fasta.gz file
    output_fasta is a .fasta or a .fasta.gz file
"""

# Modules
import gzip
import sys
import os
import re

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

# Optionally, get file containing (Genus species) to remove
try:
    species_file = sys.argv[3]
except:
    species_file = None

# Optionally, get file containing BOLD sequence IDs to remove
try:
    sequence_file = sys.argv[4]
except:
    sequence_file = None

# Iterating through sequences
print(input_fasta)
phylum = os.path.basename(input_fasta).split(".")[0].lower()
sequences = fasta_iterator(input_fasta)
found_sequences = {}
treated_sequences = 0
kept_sequences = 0
removed_species = 0
good_nuc = set("ACTGN")

# For reports
empty_sequences = 0
non_coi = 0
nine_fields = 0
no_genus = 0
non_alpha = 0
no_sp = 0
not_2_parts = 0
bad_caps = 0
too_short = 0
bad_nucs = 0
duplicate = 0

with myopen(output_fasta, "wt") as outfile:
    for s in sequences:
        treated_sequences += 1
        info = s.name.split("|")
        marker = info[1]
        taxons = info[3].split(",")

        # Remove if sequence is empty
        if not s.sequence:
            empty_sequences += 1
            continue

        # Keep only COI sequences
        if not "COI" in marker:
            non_coi += 1
            continue

        # Keep only if 9 name fields
        if len(taxons) != 9:
            nine_fields += 1
            continue

        # Keep only if genus and species info available
        if taxons[7] == "None":
            no_genus += 1
            continue

        genus_species = taxons[7]
        num_names = len(genus_species.split(" "))

        # check for non-alpha characters
        if not genus_species.replace(" ", "").isalpha():
            non_alpha += 1
            continue

        # No sp.
        if "sp." in genus_species:
            no_sp += 1
            continue

        # Not two parts to genus_species
        if num_names != 2:
            not_2_parts += 1
            continue

        # Capitalized genus and lower caps species
        if not genus_species[0].isupper() or not genus_species.split(" ")[1][0].islower():
            bad_caps += 1
            continue

        # Remove leading and trailing Ns in sequences
        s.sequence = s.sequence.replace("-", "N").strip("N")

        # Remove sequences below 300 bp
        if len(s.sequence) < 300:
            too_short += 1
            continue

        # Create final sequence name
        s.name = "_".join([taxons[3], genus_species.replace(" ", "_")])

        # Remove if bad nucleotides
        if set(s.sequence).difference(good_nuc):
            bad_nucs += 1
            continue

        # Keep only one instance of each sequence for each species
        if genus_species in found_sequences:
            if s.sequence in found_sequences[genus_species]:
                duplicate += 1
                continue
            else:
                found_sequences[genus_species].add(s.sequence)
        else:
            found_sequences[genus_species] = set(s.sequence)

        # Keep if not too many Ns
        maximum_n_proportion = 0.3
        if float(s.sequence.count("N")) / float(len(s.sequence)) < maximum_n_proportion:
            s.write_to_file(outfile)
            kept_sequences += 1

# Report
percent = round(100 * kept_sequences / treated_sequences, 2)
print(f"  Kept {percent}%, {kept_sequences} / {treated_sequences} sequences")

def report_print(name, data):
    print(f"  {name.ljust(12)}:{round(100*data/treated_sequences, 2)} %")

stats = [
        ("Empty", empty_sequences),
        ("Non COI", non_coi),
        ("No genus", no_genus),
        ("Non alpha", non_alpha),
        ("No species", no_sp),
        ("Not 2 parts", not_2_parts),
        ("Bad caps", bad_caps),
        ("Too short", too_short),
        ("Bad nucs", bad_nucs),
        ("Duplicate", duplicate),
        ]

print("\nReport of lost sequences")

for info in sorted(stats, reverse=True, key=lambda x: x[1]):
    report_print(*info)
