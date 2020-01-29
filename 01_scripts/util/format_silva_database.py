#!/usr/bin/env python3
"""Prepare a fasta file from SILVA and prepare it for COI blast db

Suggested database: SILVA_123.1_SSURef_Nr99_tax_silva_trunc.fasta.gz

- Keep only 'Genus species' sequences

Usage:
    ./01_scripts/format_silva_database.py input_fasta output_fasta
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

# Iterating through sequences
sequences = fasta_iterator(input_fasta)
found_sequences = {}
treated_sequences = 0
kept_sequences = 0
good_nuc = set(list("ACGTN"))

with myopen(output_fasta, "wt") as outfile:
    for s in sequences:
        treated_sequences += 1

        info = s.name.split(";")

        # Keep only eukaryotes
        if not "Eukaryota" in info[0]:
            continue

        # Keep only Metazoa?
        if not "Metazoa" in s.name:
            continue

        try:
            phylum = info[6].lower()
        except:
            continue

        names = info[-1].split(" ")
        num_names = len(names)
        good_name = " ".join(names)

        # Genus species
        if num_names < 2:
            continue

        if num_names > 2:
            if names[2] == "subsp.":
                names = names[0:2]
            
            elif names[2] == "var.":
                names = names[0:2]

            else:
                continue

        if "sp." in names:
            continue

        # Non genus/species taxa
        if "-" in good_name:
            continue

        names = [x.replace("'", "") for x in names]

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
            #print("Specied already found: {}".format(good_name))
            if s.sequence in found_sequences[good_name]:
                #print("Same species same sequence")
                continue
            else:
                #print("Same species different sequence")
                s.sequence.replace("U", "T")
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
