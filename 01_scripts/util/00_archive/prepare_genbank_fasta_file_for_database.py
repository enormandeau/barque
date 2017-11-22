#!/usr/bin/env python
"""Prepare a fasta file from GENBANK and prepare it for 18S blast db

- Keep only 'Genus species' sequences

Usage:
    ./01_scripts/prepare_bold_fasta_file_for_database.py input_fasta output_fasta
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
        sequence = []
        name = ""
        begun = False
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if begun:
                    yield Fasta(name, "".join(sequence))
                name = line.replace(">", "")
                sequence = []
                begun = True
            else:
                sequence.append(line)
                complete_sequence = "".join(sequence)

        if name != "":
            yield Fasta(name, sequence)

# Parse user input
try:
    input_fasta = sys.argv[1]
    output_fasta = sys.argv[2]
except:
    print __doc__
    sys.exit(1)

# Iterating through sequences
sequences = fasta_iterator(input_fasta)
found_sequences = {}
treated_sequences = 0
kept_sequences = 0
too_long = 0
good_nuc = set(list("ACTGN"))

with myopen(output_fasta, "w") as outfile:
    prev = "fake_first_value"
    for s in sequences:
        # Get name informations
        treated_sequences += 1
        info = s.name.split(" ")
        names = info[1:3]
        num_names = len(names)
        good_name = " ".join(names).replace(",", "").strip()

        # Remove sequences that are too long
        if len(s.sequence) > 10000:
            too_long += 1
            continue

        # If name looks bad, try parsing differently
        if "PREDICTED" in good_name or "rDNA" in good_name or "TSA:" in good_name:
            names = info[2:4]
            num_names = len(names)
            good_name = " ".join(names).replace(",", "").strip()

        # Genus species
        if num_names < 2 or num_names > 3:
            print "wrong name number"
            continue

        if "eos-neogaeus" in good_name:
            good_name.replace("-", "")

        if "." in good_name:
            print "'.' in name"
            continue

        if ":" in good_name:
            print "':' in name"
            continue

        if "rRNA" in good_name:
            print "'rRNA' in name"
            continue

        if "(" in good_name or ")" in good_name:
            print "parenthesis in name"
            continue

        # Non genus/species taxa
        if "-" in good_name:
            print "'-' in in name"
            continue

        # Capitalized genus and lower caps species
        names = good_name.split(" ")
        if not names[0][0].isupper() or not names[1][0].islower():
            print "capitalization:", names
            continue

        # No numbers or punctuation in names
        if not names[0].isalpha() or not names[1].isalpha():
            print "punctuation:", names
            continue

        # No genus with sp.
        if good_name.endswith("_sp."):
            print "_sp:", good_name
            continue

        if good_name in found_sequences:
            #print "Specied already found: {}".format(good_name)
            if s.sequence in found_sequences[good_name]:
                print "Same species same sequence"
                continue
            else:
                #print "Same species different sequence"
                if set(s.sequence).difference(good_nuc):
                    continue

                found_sequences[good_name].append(s.sequence)
                
        else:
            found_sequences[good_name] = [s.sequence]

        # Remove "-" characters and trailing Ns
        maximum_n_proportion = 0.3
        s.name = good_name.replace(" ", "_")
        s.sequence = s.sequence.replace("-", "N").strip("N")
        if float(s.sequence.count("N")) / float(len(s.sequence)) < maximum_n_proportion:
            kept_sequences += 1
            s.write_to_file(outfile)

        if not treated_sequences % 10:
            percent_kept = 100.0 * float(kept_sequences) / treated_sequences
            print("  kept {}/{} sequences ({}%). {} were too long".format(kept_sequences,
                treated_sequences, percent_kept, too_long))

# Report
print("Treated {} sequences".format(treated_sequences))
print("   Kept {} sequences".format(kept_sequences))
