#!/usr/bin/env python
"""Summarize usearch resuls

Usage:
    ./01_scripts/07_summarize_results.py input_folder output_folder primer_file min_similarity min_length min_coverage
"""

# Modules
from collections import defaultdict
import sys
import os

# Parsing user input
try:
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    primer_file = sys.argv[3]
    min_similarity = float(sys.argv[4])
    min_length = int(sys.argv[5])
    min_coverage = int(sys.argv[6])
except:
    print __doc__
    sys.exit(1)

# Read primer_file
primers = []
with open(primer_file) as pfile:
    for line in pfile:
        if line.startswith("#"):
            continue

        l = line.strip()
        primers.append(l.split()[0])

# Read usearch results form input_folder
result_files = os.listdir(input_folder)
result_dictionary = {}

# Iterate through primers, gather taxon counts
for p in primers:
    result_dictionary[p] = {}
    primer_results = [x for x in result_files if p in x]

    # Iterate through result files for primer
    for res in primer_results:
        sample = res.split("_")[0]
        result_dictionary[p][sample] = defaultdict(int)

        # Get infos form result file
        with open(os.path.join(input_folder, res)) as rfile:
            for line in rfile:
                l = line.strip().split()
                taxon = l[1] # "_".join(l[1].split("_")[0:3])
                similarity = float(l[2])
                length = int(l[3])

                if similarity >= min_similarity and length >= min_length:
                    result_dictionary[p][sample][taxon] += 1

# Get represented taxons
taxon_dict = {}
for p in result_dictionary:
    taxon_dict[p] = set()
    for sample in result_dictionary[p]:
        for taxon in result_dictionary[p][sample]:
            count = result_dictionary[p][sample][taxon]
            if count > 1:
                taxon_dict[p].add(taxon)

    taxon_dict[p] = sorted(list(taxon_dict[p]))

# Summarize results
for p in sorted(result_dictionary):

    # Create header line
    result_table = [["Phylum\tGenus\tSpecies"]]
    for sample in sorted(result_dictionary[p]):
        result_table[0].append(sample)

    # Add rows
    for taxon in taxon_dict[p]:
        result_table.append(["\t".join(taxon.split("_"))])
        for sample in sorted(result_dictionary[p]):
            count = result_dictionary[p][sample][taxon]
            result_table[-1].append(str(count))

    # Print results to file
    with open(os.path.join(output_folder, p + "_results.csv"), "w") as outfile:
        for line in result_table:
            prepared_line = "\t".join(line) + "\n"

            if prepared_line.startswith("Phylum"):
                outfile.write(prepared_line)

            elif max([int(x) for x in line[3:]]) > min_coverage:
                outfile.write(prepared_line)
