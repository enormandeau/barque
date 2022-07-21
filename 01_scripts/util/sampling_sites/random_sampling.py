#!/usr/bin/env python3
"""In species table from Barque, identify n random sites and compute nspecies

This script is used to assist in finding better sampling plans in lakes.

WARNING! Treat species table to keep only species of interest:
    - Remove non-fish species if you are interested only in fish
    - Resolve multiple hits (merge with existing species if needed)
    - Filter to remove potential false positives

NOTE: Need to find a good way to assess diversity
    - RECOMMENDED: Presence/absence (with possible filters, eg: min reads, min samples)
    - Shannon index? (May maximize shannon while loosing more species) (may create biases)
    - Presence but favor species with more reads (sqrt(reads)) (may create biases)

Usage:
    <program> input_table num_iter output_file
"""
# Modules
from collections import Counter, defaultdict
from random import random, sample
from math import sqrt, exp
from numpy import std
import sys

# Functions
def compute_score_num_species(solution, min_reads=10):
    """Return number of counted species from SA solution

    Recommended score function.
    """
    species = [list(x)[:] for x in list(zip(*solution))][1: ]
    score = 0.0
    for s in species:
        score += 1 if len([x for x in s if x >= min_reads]) else 0

    return score

# Parse user input
try:
    input_table = sys.argv[1]
    num_iter = int(sys.argv[2])
    output_file = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Read table count
with open(input_table) as infile:
    lines = [line.strip().split(",") for line in infile]

    if not lines[0][3] == "Total":
        print("Wrong format. The 4 first columns should be named:")
        print("'Group', 'Genus', 'Species', 'Total'")
        sys.exit(1)

    transposed = list(zip(*lines))

    header = transposed[:6]
    data = [list(x) for x in transposed[4: ]]

    for d in data:
        d[1: ] = [int(x) for x in d[1: ]]

# Initialize dictionary
counts = defaultdict(list)
num_sites = len(data)

#score = compute_score(solution)
for n in range(1, num_sites+1):
    for i in range(1, num_iter+1):

        # Sample n sites randomly from data
        subsample = sample(data, n)

        # Count number of species and add to counts dictionary
        num_species = compute_score_num_species(subsample)
        counts[n].append(num_species)

# Produce report
with open(output_file, "wt") as outfile:
    # Header
    outfile.write("RandNsites\tRandMean\tRandStd\n")
    for n in counts:
        avg = sum(counts[n]) / len(counts[n])
        sd = std(counts[n])
        outfile.write("\t".join([str(n), str(round(avg, 4)), str(round(sd, 4))]) + "\n")
