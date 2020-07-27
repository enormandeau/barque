#!/usr/bin/env python

"""Split amplicons using forward and reverse potentially degenerated primers

Usage:
    %program fastq_file primer_file iupac_file output_folder max_distance
"""

# Importing modules
from collections import defaultdict
import gzip
import sys
import re
import os

# Defining classes
class Fastq(object):
    """Fastq object with name and sequence
    """
    def __init__(self, name, seq, name2, qual):
        self.name = str(name)
        self.seq = str(seq)
        self.name2 = str(name2)
        self.qual = str(qual)
    def write_to_file(self, handle):
        handle.write("@" + self.name + "\n")
        handle.write(self.seq + "\n")
        handle.write("+" + self.name2 + "\n")
        handle.write(self.qual + "\n")
    def __repr__(self):
        return "\t".join([self.seq[0:51], self.seq[0:51]])

# Defining functions
def myopen(infile, mode="rt"):
    if infile.endswith(".gz"):
        return gzip.open(infile, mode=mode)
    else:
        return open(infile, mode=mode)

def fastq_iterator(input_file):
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

def reverse_complement(seq):
    complement =  {
            "A":"T",
            "C":"G",
            "G":"C",
            "T":"A",
            "[":"]",
            "]":"[",
            "(":")",
            ")":"("
            }

    comp = []
    for s in seq:
        if s in complement:
            comp.append(complement[s])
        else:
            comp.append(s)

    return "".join(comp[::-1])

def replace_iupac(seq):
    temp = []
    for s in seq:
        if s in iupac:
            temp.append(iupac[s])
        else:
            temp.append(s)

    return "".join(temp)

def find_primer(primer, sequence, reverse=False):
    if reverse:
        sequence = reverse_complement(sequence)

    pad = "NN"
    padded_primer = pad + primer + pad
    best_distance = 99
    best_position = 99

    for i in range(1 + 2*len(pad)):
        subsequence = sequence[: len(primer)]
        subprimer = padded_primer[i: i + len(primer)]
        distance = iupac_distance(subsequence, subprimer)
        if distance < best_distance:
            best_distance = distance
            best_position = i

    return best_distance, best_position - len(pad)

def iupac_distance(sequence, primer):
    assert len(sequence) == len(primer), "Sequences to be compared must have the same length"
    dist = 0
    dist_string = ""

    for i in range(len(sequence)):
        if sequence[i] not in iupac[primer[i]]:
            dist += 1
            dist_string += "^"
        else:
            dist_string += " "

    return dist

# Parsing user input
try:
    fastq_file = sys.argv[1]
    primer_file = sys.argv[2]
    iupac_file = sys.argv[3]
    output_folder = sys.argv[4]
    max_distance = int(sys.argv[5])
except:
    print(__doc__)
    sys.exit(0)

# Main
## parse iupac
iupac = {}
with open(iupac_file) as pfile:
    for line in pfile:
        name, sequence = line.strip().split(",")
        iupac[name] = sequence

## Parse primers
primers = {}
with open(primer_file) as pfile:
    for line in pfile:
        # Skip comment lines
        if line.startswith("#"):
            continue

        if not line.strip():
            continue

        # Get primer infos
        name, forward, reverse, min_length, max_length, database, simil_species, simil_genus, simil_phylum = line.strip().split(",")
        forward_length = len(forward)
        reverse_length = len(reverse)

        primers[name] = (forward, reverse, int(min_length), int(max_length), forward_length, reverse_length)

## Open output fastq.gz files
output_files = {}
input_file = os.path.basename(fastq_file)

# Add fake primers to automatically open file handles
primers["not_found"] = "FAKE"
primers["forward_only"] = "FAKE"
primers["too_short"] = "FAKE"
primers["too_long"] = "FAKE"

# Open output file handles
for p in primers:
    output_files[p] = myopen(os.path.join(output_folder, input_file.replace(".fastq", "_" + p + ".fastq")), "wt")

## Prepare summary of splitting
primers_summary = defaultdict(int)

## Read fastq file
sequences = fastq_iterator(fastq_file)
num_treated = 0
num_extracted = 0
forward_orientation = 0
reverse_orientation = 0

for s in sequences:
    num_treated += 1
    sequence_found = False
    reverse_s = reverse_complement(s.seq)

    for p in primers:

        # Skip fake primers
        if primers[p] == "FAKE":
            continue

        forward, reverse, min_length, max_length, forward_length, reverse_length = primers[p]

        # Look for primers in forward-reverse order
        forward_dist, forward_position = find_primer(forward, s.seq, reverse=False)
        reverse_dist, reverse_position = find_primer(reverse, s.seq, reverse=True)

        # Look for primers in reverse-forward order
        forward_dist_rev, forward_position_rev = find_primer(forward, reverse_s, reverse=False)
        reverse_dist_rev, reverse_position_rev = find_primer(reverse, reverse_s, reverse=True)

        # Check if both primers are found with an acceptable number of differences
        if forward_dist > max_distance and forward_dist_rev > max_distance:
            s.write_to_file(output_files["not_found"])
            primers_summary["not_found"] += 1
            continue

        if reverse_dist > max_distance and reverse_dist_rev > max_distance:
            s.write_to_file(output_files["forward_only"])
            primers_summary["forward_only"] += 1
            continue

        # Check that amplicon length is good
        amplicon_length = len(s.seq) - forward_length - reverse_length

        if amplicon_length < min_length:
            s.write_to_file(output_files["too_short"])
            primers_summary["too_short"] += 1
            continue

        if amplicon_length > max_length:
            s.write_to_file(output_files["too_long"])
            primers_summary["too_long"] += 1
            continue

        # If primers found in the reverse-forward order, reverse the sequence
        if forward_dist_rev < forward_dist:
            reverse_orientation += 1
            s.seq = reverse_complement(s.seq)
            s.qual = s.qual[::-1]
        else:
            forward_orientation +=1

        # Extract amplicon
        left = forward_length + forward_position
        right = len(s.seq) - (reverse_length + reverse_position)
        s.seq  =  s.seq[left: right]
        s.qual = s.qual[left: right]

        # Write to file
        s.write_to_file(output_files[p])
        primers_summary[p] += 1
        num_extracted += 1

## Write summary file
with open(os.path.join(output_folder, input_file.replace(".fastq.gz", "_summary.csv")), "wt") as summary:

    # Write sample name
    sample_name = input_file.split("_")[0]
    summary.write(",".join(["Primer", sample_name]) + "\n")

    # Wanted amplicons
    for p in sorted(primers_summary):
        if primers[p] != "FAKE":
            summary.write(",".join([p, str(primers_summary[p])]) + "\n")

    # Filtered sequences
    for p in ["not_found", "forward_only", "too_long", "too_short"]:
        if primers[p] == "FAKE":
            summary.write(",".join([p, str(primers_summary[p])]) + "\n")

## Report success
filename = fastq_file.split("/")[-1]
if num_treated == 0:
    print("Extracted 0% (0/0)\t\tof the sequences ({})".format(filename))
else:
    print("Extracted {}% ({}/{})\tof the sequences, {}% in forward orientation ({})".format(str(100.0 *float(num_extracted)/num_treated)[0:4], num_extracted, num_treated, str(100.0 * forward_orientation / (forward_orientation + reverse_orientation))[0:4], filename))

## Close file handles
for f in output_files:
    output_files[f].close()
