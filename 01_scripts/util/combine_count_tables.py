#!/usr/bin/env python3
"""Combine species/genus/phylum count tables

Usage:
    <program> input_table1 input_table2 output_table

WARNING:
    Merged tables need to have the same number of samples and be at the same
    taxonomic level (ex: species with species, genus with genus...).

    For the results to make sense, merged tables should be from the same locus.
"""

# Modules
from operator import add
import sys

# Parsing user input
try:
    input_table1 = sys.argv[1]
    input_table2 = sys.argv[2]
    output_table = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Read both tables
with open(input_table1) as in_table1:
    table1 = [x.strip().split(",") for x in in_table1.readlines()]

with open(input_table2) as in_table2:
    table2 = [x.strip().split(",") for x in in_table2.readlines()]

# Confirm taxonomic levels
if table1[0][0:4].index("Total") != table2[0][0:4].index("Total"):
    print("Error: Tables are not of the same taxonomic level")

# Confirm column numbers
if table1[0] != table2[0]:
    print("Error: Tables should contain the same number and name of columns")

# Merge
merged = dict()
key_length = table1[0][0:4].index("Total")

for species_counts in table1[1:]:
    key = tuple(species_counts[0: key_length])
    data = [int(x) for x in species_counts[key_length: ]]
    merged[key] = data

for species_counts in table2[1:]:
    key = tuple(species_counts[0: key_length])
    data = [int(x) for x in species_counts[key_length: ]]
    if key in merged:
        merged[key] = map(add, data, merged[key])
    else:
        merged[key] = data

# Write output
with open(output_table, "w") as out_table:
    out_table.write(",".join(table1[0]) + "\n")

    for key in sorted(merged):
        out_table.write(",".join(list(key) + [str(x) for x in merged[key]]) + "\n")
