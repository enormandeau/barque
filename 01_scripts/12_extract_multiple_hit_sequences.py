#!/usr/bin/env python3
"""Extract database and sample sequences for multiple hit groups

Usage:
    <program> config_file
"""

# Modules
from collections import defaultdict
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

    def __repr__(self):
        return self.name + " " + self.sequence[:31]

# Defining functions
def myopen(_file, mode="rt"):
    if _file.endswith(".gz"):
        return gzip.open(_file, mode=mode)

    else:
        return open(_file, mode=mode)

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

# Parse user input
try:
    config_file = sys.argv[1]
except:
    print(__doc__)
    sys.exit(1)

# Read config file
primer_file = [x for x in open(config_file).readlines() if "PRIMER_FILE" in x][0]
primer_file = primer_file.split("#")[0].split("=")[1].strip().replace('"', '')

# Read primer file
primers = [x for x in open(primer_file).readlines() if not x.startswith("#")]
primers = [(x.split(",")[0], x.split(",")[5]) for x in primers]

# Read Multiple Hit Groups info
for primer in primers:
    multihit_file = "12_results/" + primer[0] + "_multiple_hit_infos.csv"
    multihits = open(multihit_file).readlines()
    multihits = [x.strip().split(",") for x in multihits]
    multihits_dict = defaultdict(list)

    for multihit in multihits:
        multihits_dict[multihit[0]].append((multihit[1], multihit[2]))

    # Get all the species and genus of interest
    species_set = set()
    genus_set = set()

    for species_group in [x[0].split(";") for x in multihits]:
        for species in species_group:
            species_set.add(species)
            genus_set.add(species.split("_")[1])

    # Get all wanted sequences from database
    db_sequences = fasta_iterator("03_databases/" + primer[1] + ".fasta.gz")
    genus_sequences = defaultdict(list)

    for s in db_sequences:
        genus = s.name.split("_")[1]
        if genus in genus_set:
            genus_sequences[genus].append(s)
    
    # Get all wanted sequences per sample
    samples = sorted(list(set([x[1] for x in multihits])))
    sequence_names_per_sample = defaultdict(set)

    for multihit in multihits:
        sequence_names_per_sample[multihit[1]].add(multihit[2])

    sample_sequences = dict()

    for sample in samples:
        sequences = fasta_iterator("08_chimeras/" + sample + "_merged_" +
                primer[0] + "_nonchimeras.fasta.gz_unique.fasta.gz")

        for s in sequences:
            if s.name in sequence_names_per_sample[sample]:
                sample_sequences[(sample, s.name)] = s

    # Write sequences of multihit groups to files
    multihit_num = 0

    for multihit in multihits_dict:
        multihit_num += 1
        wanted_sequences = []
        wanted_genus = list(set([x.split("_")[1] for x in multihit.split(";")]))

        # Get sequences from database
        for genus in wanted_genus:
            wanted_sequences += genus_sequences[genus]

        # Get sequences from samples
        multihit_info = multihits_dict[multihit]

        for sequence_info in multihit_info:
            sample_name = sequence_info[0]
            s = sample_sequences[sequence_info]
            s.name = sample_name + "_" + s.name
            wanted_sequences.append(s)

        with myopen("12_results/01_multihits/" + primer[0] + "_" + "multihit_group_" + str(multihit_num) + ".fasta", "wt") as outfile:
            for s in wanted_sequences:
                s.write_to_file(outfile)
