#!/usr/bin/env python3
"""Reduce the table of multiple hits by group of shared species

Usage:
    <program> inputFile outputFile
"""

# Modules
from collections import defaultdict
import sys

# Parsing user input
try:
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
except:
    print(__doc__)
    sys.exit(1)

# Create dictionary of species lists and counts
groups = list()
all_species = set()
species_dict = defaultdict(list)

with open(inputFile) as infile:
    for line in infile:
        l = line.strip().split(",")
        count, species = l
        species = species.split(";")
        groups.append((count, species))

        for s in species:
            all_species.add(s)
            species_dict[s].append((count, species))

# Reduce species lists and cumulate counts
for sp in all_species:
    species_group = []

    # Combine all groups that contain a species
    for n, g in enumerate(groups):
        if sp in g[1]:
            species_group.append(groups.pop(n))

    # Compute new sum and new species list
    count = sum([int(x[0]) for x in species_group])
    species = [x[1] for x in species_group]

    # Flatten, make unique, and sort
    species = sorted(list(set([val for sublist in species for val in sublist])))

    # Add new compound group to list
    groups = [(count, species)] + groups

# Sort by presence
groups = [(int(g[0]), g[1]) for g in groups]
groups = sorted(groups, reverse=True)

# Prepare string for output
groups = [str(g[0]) + "," + ";".join(g[1]) + "\n" for g in groups]

with open(outputFile, "w") as outfile:
    for g in groups:
        outfile.write(g)
