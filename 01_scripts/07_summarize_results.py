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
species_dictionary = {}
genus_dictionary = {}
phylum_dictionary = {}

# Iterate through primers, gather taxon counts
for primer in primers:
    species_dictionary[primer] = {}
    genus_dictionary[primer] = {}
    phylum_dictionary[primer] = {}
    primer_results = [filename for filename in result_files if primer in filename]

    # Iterate through result files for primer
    for result_file in primer_results:
        sample = result_file.split("_")[0]
        species_dictionary[primer][sample] = defaultdict(int)
        genus_dictionary[primer][sample] = defaultdict(int)
        phylum_dictionary[primer][sample] = defaultdict(int)

        # Get infos form result file
        with open(os.path.join(input_folder, result_file)) as rfile:
            for line in rfile:
                l = line.strip().split()
                species = l[1] # "_".join(l[1].split("_")[0:3])
                similarity = float(l[2])
                length = int(l[3])

                if similarity >= min_similarity and length >= min_length:
                    # Species
                    species_dictionary[primer][sample][species] += 1

                    # Genus
                    genus = "_".join(species.split("_")[0:2])
                    genus_dictionary[primer][sample][genus] += 1

                    # Phylum
                    phylum = "_".join(species.split("_")[0:1])
                    phylum_dictionary[primer][sample][phylum] += 1

# Get represented taxons
species_found = {}
genus_found = {}
phylum_found = {}

for primer in species_dictionary:
    species_found[primer] = set()
    genus_found[primer] = set()
    phylum_found[primer] = set()

    for sample in species_dictionary[primer]:
        for species in species_dictionary[primer][sample]:
            count = species_dictionary[primer][sample][species]
            if count > 0:
                # Species
                species_found[primer].add(species)

                # Genus
                genus = "_".join(species.split("_")[0:2])
                genus_found[primer].add(genus)

                # Phylum
                phylum = "_".join(species.split("_")[0:1])
                phylum_found[primer].add(phylum)

    species_found[primer] = sorted(list(species_found[primer]))
    genus_found[primer] = sorted(list(genus_found[primer]))
    phylum_found[primer] = sorted(list(phylum_found[primer]))

# Summarize results
for primer in sorted(species_dictionary):

    # Create header line
    species_table = [["Phylum\tGenus\tSpecies"]]
    genus_table = [["Phylum\tGenus"]]
    phylum_table = [["Phylum"]]

    for sample in sorted(species_dictionary[primer]):
        species_table[0].append(sample)
        genus_table[0].append(sample)
        phylum_table[0].append(sample)

    # Add rows to table
    # Species
    for species in species_found[primer]:
        species_table.append(["\t".join(species.split("_"))])
        for sample in sorted(species_dictionary[primer]):
            count = species_dictionary[primer][sample][species]
            species_table[-1].append(str(count))

    # Genus
    for genus in genus_found[primer]:
        genus_table.append(["\t".join(genus.split("_"))])
        for sample in sorted(genus_dictionary[primer]):
            count = genus_dictionary[primer][sample][genus]
            genus_table[-1].append(str(count))

    # Phylum
    for phylum in phylum_found[primer]:
        phylum_table.append(["\t".join(phylum.split("_"))])
        for sample in sorted(phylum_dictionary[primer]):
            count = phylum_dictionary[primer][sample][phylum]
            phylum_table[-1].append(str(count))

    # Print results to file
    # Species
    with open(os.path.join(output_folder, primer + "_species_results.csv"), "w") as outfile:
        for line in species_table:
            prepared_line = "\t".join(line) + "\n"

            if prepared_line.startswith("Phylum"):
                outfile.write(prepared_line)

            elif max([int(x) for x in line[3:]]) > min_coverage:
                outfile.write(prepared_line)

    # Species
    with open(os.path.join(output_folder, primer + "_genus_results.csv"), "w") as outfile:
        for line in genus_table:
            prepared_line = "\t".join(line) + "\n"

            if prepared_line.startswith("Phylum"):
                outfile.write(prepared_line)

            elif max([int(x) for x in line[2:]]) > min_coverage:
                outfile.write(prepared_line)

    # Species
    with open(os.path.join(output_folder, primer + "_phylum_results.csv"), "w") as outfile:
        for line in phylum_table:
            prepared_line = "\t".join(line) + "\n"

            if prepared_line.startswith("Phylum"):
                outfile.write(prepared_line)

            elif max([int(x) for x in line[1:]]) > min_coverage:
                outfile.write(prepared_line)
