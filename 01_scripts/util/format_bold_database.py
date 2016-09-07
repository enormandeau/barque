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

# Iterating through sequences
phylum = os.path.basename(input_fasta).split(".")[0].lower()
sequences = fasta_iterator(input_fasta)
found_sequences = {}
treated_sequences = 0
kept_sequences = 0
good_nuc = set(list("ACTGN"))

with myopen(output_fasta, "w") as outfile:
    for s in sequences:
        treated_sequences += 1
        info = s.name.split("|")
        names = info[1].split(" ")
        num_names = len(names)
        good_name = " ".join(names)

        # Genus species
        if num_names < 2 or num_names > 3:
            continue

        if "eos-neogaeus" in good_name:
            good_name.replace("-", "")

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

        if good_name in found_sequences:
            #print "Specied already found: {}".format(good_name)
            if s.sequence in found_sequences[good_name]:
                #print "Same species same sequence"
                continue
            else:
                #print "Same species different sequence"
                if set(s.sequence).difference(good_nuc):
                    continue

                found_sequences[good_name].append(s.sequence)
                
        else:
            found_sequences[good_name] = [s.sequence]

        kept_sequences += 1

        # Remove "-" characters and trailing Ns
        maximum_n_proportion = 0.3
        s.name = good_name.replace(" ", "_")
        s.name = phylum + "_" + s.name
        s.sequence = s.sequence.replace("-", "N").strip("N")
        if float(s.sequence.count("N")) / float(len(s.sequence)) < maximum_n_proportion:
            s.write_to_file(outfile)

# Report
print("Treated {} sequences".format(treated_sequences))
print("   Kept {} sequences".format(kept_sequences))
