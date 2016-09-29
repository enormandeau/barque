#!/usr/bin/env python
"""Prepare a fasta file from BOLD and prepare it for COI blast db

- Keep only 'Genus species' sequences

Usage:
    ./01_scripts/format_bold_database.py input_fasta output_fasta
"""

# Modules
import gzip
import sys
import os

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

# Functions
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
    input_fasta = sys.argv[1]
    output_fasta = sys.argv[2]
except:
    print __doc__
    sys.exit(1)

# Optionally, get file containing (Genus species) to remove
try:
    species_file = sys.argv[3]
except:
    species_file = None

# Create set of unwanted species
if species_file:
    species_set = set()
    with open(species_file) as sfile:
        for line in sfile:
            l = line.strip().replace(" ", "_")
            species_set.add(l)
else:
    species_set = None

# Iterating through sequences
print input_fasta
phylum = os.path.basename(input_fasta).split(".")[0].lower()
sequences = fasta_iterator(input_fasta)
found_sequences = {}
treated_sequences = 0
kept_sequences = 0
removed_species = 0
good_nuc = set("ACTGN")

with myopen(output_fasta, "w") as outfile:
    for s in sequences:
        treated_sequences += 1
        info = s.name.split("|")
        names = info[1].split(" ")
        num_names = len(names)
        good_name = " ".join(names)

        # Keep only COI sequences
        if not "COI" in s.name:
            continue

        # Genus species
        if num_names < 2 or num_names > 3:
            continue

        if "eos-neogaeus" in good_name:
            good_name.replace("-", "")

        # Remove sequences with '-' characters
        if "-" in s.sequence:
            continue

        # Non genus/species taxa
        if "-" in good_name:
            continue

        # Capitalized genus and lower caps species
        if not names[0][0].isupper() or not names[1][0].islower():
            continue

        # No numbers or punctuation in names
        if not names[0].isalpha() or not names[1].isalpha():
            continue

        # No genus with sp.
        if good_name.endswith("_sp."):
            continue

        # Trim names with more than 2 fields
        if len(good_name.split(" ")) > 2:
            good_name = "_".join(good_name.split(" ")[0:2])

        # Remove leading and trailing Ns
        s.sequence = s.sequence.replace("-", "N").strip("N")

        # Remove sequences below 300 bp
        if len(s.sequence) < 300:
            continue

        # Create final sequence name
        s.name = good_name.replace(" ", "_")

        # Remove unwanted species
        if species_set:
            if s.name in species_set:
                removed_species += 1
                continue

        # Remove Homo_sapiens
        if s.name == "Homo_sapiens":
            continue

        # Adding phylum name
        s.name = phylum + "_" + s.name

        # Remove if bad nucleotides
        if set(s.sequence).difference(good_nuc):
            continue

        if good_name in found_sequences:
            #print "Species already found: {}".format(good_name)
            if s.sequence in found_sequences[good_name]:
                #print "Same species same sequence"
                continue
            else:
                #print "Same species different sequence"
                found_sequences[good_name].append(s.sequence)
                
        else:
            found_sequences[good_name] = [s.sequence]

        # Keep if not too many Ns
        maximum_n_proportion = 0.3
        if float(s.sequence.count("N")) / float(len(s.sequence)) < maximum_n_proportion:
            s.write_to_file(outfile)
            kept_sequences += 1

# Report
print("Treated {} sequences".format(treated_sequences))
print("   Kept {} sequences".format(kept_sequences))
print("   Removed {} sequences from unwanted species".format(removed_species))
print("")
