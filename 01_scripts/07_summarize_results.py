#!/usr/bin/env python
"""Summarize vsearch results

Usage:
    ./01_scripts/07_summarize_results.py input_folder output_folder primer_file min_length min_coverage

Where:
    input_folder is '09_vsearch'
    output_folder is '12_results'
    primer_file is '02_info/primers.csv'
    min_length is the minimum length of the hits to keep (typically >= 100)
    min_coverage is the minimun number of hits a taxon (species, genus or phylum)
        must have in *at least* one sample in order for the taxon to be kept
"""

# Modules
from collections import defaultdict
import gzip
import sys
import os

# Defining functions
def myopen(infile, mode="rt"):
    if infile.endswith(".gz"):
        return gzip.open(infile, mode=mode)
    else:
        return open(infile, mode=mode)

# Parsing user input
try:
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    primer_file = sys.argv[3]
    min_length = int(sys.argv[4])
    min_coverage = int(sys.argv[5])
except:
    print(__doc__)
    sys.exit(1)

# Read primer_file
primers = dict()
with open(primer_file) as pfile:
    for line in pfile:
        if line.startswith("#"):
            continue

        l = line.strip().split(",")
        primers[l[0]] = l[5]

# Read vsearch results form input_folder
result_files = os.listdir(input_folder)
species_dictionary = {}
genus_dictionary = {}
phylum_dictionary = {}

# Iterate through primers, gather taxon counts
for primer in primers:
    multiple_hits = defaultdict(int)

    # Get minimum similarity for the primer
    primer_info = [x.strip().split(",") for x in open(primer_file).readlines() if x.startswith(primer + ",")][0]
    min_similarity = 100 * float(primer_info[6])

    # Create summary dictionary
    species_dictionary[primer] = {}
    genus_dictionary[primer] = {}
    phylum_dictionary[primer] = {}

    # List result files for primer
    primer_results = [filename for filename in result_files if "_" + primer + "_" in filename]
    primer_results = [filename for filename in primer_results if not filename.endswith("_matched.fasta.gz")]

    # Iterate through result files for primer
    for result_file in primer_results:
        sample = result_file.split("_")[0]
        species_dictionary[primer][sample] = defaultdict(int)
        genus_dictionary[primer][sample] = defaultdict(int)
        phylum_dictionary[primer][sample] = defaultdict(int)

        # Get infos form result file
        seen = set()
        sequence_dict = defaultdict(list)
        sequence_list = []

        # Read all hits for each sequence into a dictionary
        with myopen(os.path.join(input_folder, result_file)) as rfile:
            for line in rfile:
                sequence_name = line.split()[0]
                sequence_dict[sequence_name].append(line.strip().split()[1:])
                if not sequence_name in seen:
                    seen.add(sequence_name)
                    sequence_list.append(sequence_name)

        # Treat each sequence
        for seq in sequence_list:
            count = int(seq.split("_")[3])
            best_score = min([float(x[1]) for x in sequence_dict[seq]])
            best_species = set([x[0] for x in sequence_dict[seq]
                if (float(x[1]) == best_score
                    and float(x[1]) >= min_similarity
                    and int(x[2]) >= min_length)])

            # Species level identification
            if len(best_species) == 1:
                species = list(best_species)[0]
                species_dictionary[primer][sample][species] += count

                genus = "_".join(list(best_species)[0].split("_")[:2])
                genus_dictionary[primer][sample][genus] += count

                phylum = list(best_species)[0].split("_")[0]
                phylum_dictionary[primer][sample][phylum] += count

            elif len(best_species) > 1:
                # Summaryze multiple hits
                multiple_hits[";".join(sorted(list(best_species)))] += count

                # Genus level identification
                if len(set([x.split("_")[1] for x in best_species])) == 1:
                    genus = "_".join(list(best_species)[0].split("_")[:2])
                    genus_dictionary[primer][sample][genus] += count

                    phylum = list(best_species)[0].split("_")[0]
                    phylum_dictionary[primer][sample][phylum] += count

                # Phylum level identification
                else:
                    phylum = list(best_species)[0].split("_")[0]
                    phylum_dictionary[primer][sample][phylum] += count

    # Write multiple hit summary
    lines = []
    for group in sorted(multiple_hits.keys()):
        lines.append((multiple_hits[group], group))

    lines = sorted(lines, reverse=True)
    lines = [str(x[0]) + "," + x[1] for x in lines]

    with open(os.path.join(output_folder, "multiple_hits_" + primer + "_" + primers[primer] + ".csv"), "w") as outfile:
        for l in lines:
            outfile.write(l + "\n")

# Get represented taxons
species_found = {}
for primer in species_dictionary:
    species_found[primer] = set()

    for sample in species_dictionary[primer]:
        for species in species_dictionary[primer][sample]:
            count = species_dictionary[primer][sample][species]
            if count > 0:
                # Species
                species_found[primer].add(species)

    species_found[primer] = sorted(list(species_found[primer]))

genus_found = {}
for primer in genus_dictionary:
    genus_found[primer] = set()

    for sample in genus_dictionary[primer]:
        for genus in genus_dictionary[primer][sample]:
            count = genus_dictionary[primer][sample][genus]
            if count > 0:

                # Genus
                genus_found[primer].add(genus)

    genus_found[primer] = sorted(list(genus_found[primer]))

phylum_found = {}
for primer in phylum_dictionary:
    phylum_found[primer] = set()

    for sample in phylum_dictionary[primer]:
        for phylum in phylum_dictionary[primer][sample]:
            count = phylum_dictionary[primer][sample][phylum]
            if count > 0:

                # Phylum
                phylum_found[primer].add(phylum)

    phylum_found[primer] = sorted(list(phylum_found[primer]))

# Summarize results
for primer in sorted(species_dictionary):

    # Create header line
    species_table = [["Phylum,Genus,Species,Total"]]
    genus_table = [["Phylum,Genus,Total"]]
    phylum_table = [["Phylum,Total"]]

    for sample in sorted(species_dictionary[primer]):
        species_table[0].append(sample)
        genus_table[0].append(sample)
        phylum_table[0].append(sample)

    # Add rows to table
    # Species
    for species in species_found[primer]:
        species_table.append([",".join(species.split("_"))])
        count_sum = 0
        new_line = []
        for sample in sorted(species_dictionary[primer]):
            count = species_dictionary[primer][sample][species]
            count_sum += count
            new_line.append(str(count))
        species_table[-1].append(str(count_sum))
        species_table[-1] += new_line

    # Genus
    for genus in genus_found[primer]:
        genus_table.append([",".join(genus.split("_"))])
        count_sum = 0
        new_line = []
        for sample in sorted(genus_dictionary[primer]):
            count = genus_dictionary[primer][sample][genus]
            count_sum += count
            new_line.append(str(count))
        genus_table[-1].append(str(count_sum))
        genus_table[-1] += new_line

    # Phylum
    for phylum in phylum_found[primer]:
        phylum_table.append([",".join(phylum.split("_"))])
        count_sum = 0
        new_line = []
        for sample in sorted(phylum_dictionary[primer]):
            count = phylum_dictionary[primer][sample][phylum]
            count_sum += count
            new_line.append(str(count))
        phylum_table[-1].append(str(count_sum))
        phylum_table[-1] += new_line

    # Print results to file
    # Species
    with open(os.path.join(output_folder, primer + "_species_table.csv"), "wt") as outfile:
        for line in species_table:
            prepared_line = ",".join(line) + "\n"

            if prepared_line.startswith("Phylum"):
                outfile.write(prepared_line)

            elif max([int(x) for x in line[3:]]) > min_coverage:
                outfile.write(prepared_line)

    # Genus
    with open(os.path.join(output_folder, primer + "_genus_table.csv"), "wt") as outfile:
        for line in genus_table:
            prepared_line = ",".join(line) + "\n"

            if prepared_line.startswith("Phylum"):
                outfile.write(prepared_line)

            elif max([int(x) for x in line[2:]]) > min_coverage:
                outfile.write(prepared_line)

    # Phylum
    with open(os.path.join(output_folder, primer + "_phylum_table.csv"), "wt") as outfile:
        for line in phylum_table:
            prepared_line = ",".join(line) + "\n"

            if prepared_line.startswith("Phylum"):
                outfile.write(prepared_line)

            elif max([int(x) for x in line[1:]]) > min_coverage:
                outfile.write(prepared_line)
