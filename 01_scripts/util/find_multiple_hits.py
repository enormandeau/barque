#!/usr/bin/env python
"""Report number of reads with multiple hits with species

Usage:
    ./01_scripts/util/find_multiple_hits.py inputFolder database outputFile
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
    inputFolder = sys.argv[1]
    database = sys.argv[2]
    outputFile = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Iterate through files
result_files = os.listdir(inputFolder)
result_files = [x for x in result_files if x.endswith(database + ".gz")]

species_dict = defaultdict(list)

for result_file in result_files:
    with myopen(os.path.join(inputFolder, result_file), "rt") as rfile:
        hits = defaultdict(list)
        for line in rfile:
            l = line.strip().split()
            sequence = l[0]
            species = l[1]
            similarity = float(l[2])
            hits[sequence].append((similarity, species))

        for k, v in hits.items():
            if len(set(v)) > 1:
                # Keep only these who have an the highest similarity
                v = sorted(v, reverse=True)
                max_similarity = v[0][0]
                v = [x for x in v if x[0] == max_similarity]

                # Remove similarity
                v = [x[1] for x in v]

                # Sort species in a predictable manner
                sp_group = tuple(sorted(list(set(v))))

                # Add species to species_dict
                species_dict[sp_group].append(k)

# Count occurences of multiple hits
multiple_hits = []
for s in species_dict:
    if len(s) > 1:
        multiple_hits.append((sum([int(x.split("_")[3]) for x in species_dict[s]]), ";".join(s)))

sorted_multiple_hits = sorted(multiple_hits, reverse=True)

# Write results to file
with myopen(outputFile, "wt") as outfile:
    for species in sorted_multiple_hits:
        outfile.write(str(species[0]) + "," + species[1] + "\n")
