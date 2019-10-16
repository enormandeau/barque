#!/usr/bin/env python3
"""Format db_teleo1.fasta provided by Laetitia

Usage:
    <program> input_db output_db

Name format:
    >KX148472 family_name=Zoarcidae; species_name=Lycodes tanakae; family=8193; taxid=1358735; genus_name=Lycodes; rank=species; genus=8196; species=1358735;     Lycodes tanakae mitochondrion, complete genome
"""

# Modules
import gzip
import sys

# Functions
def myopen(_file, mode="rt"):
    if _file.endswith(".gz"):
        return gzip.open(_file, mode=mode)

    else:
        return open(_file, mode=mode)

# Parse user input
try:
    input_db = sys.argv[1]
    output_db = sys.argv[2]
except:
    print(__doc__)
    sys.exit(1)

# Process db
with myopen(input_db) as infile:
    with myopen(output_db, "wt") as outfile:
        for line in infile:
            if line.startswith(">"):
                l = line.strip().split(";")
                family_name = l[0].split("=")[1]
                species_name = l[1].split("=")[1].split(".")[0]
                taxon = family_name + "_" + species_name.replace(" ", "_")
                taxon = taxon.replace("###", "unknown_unknown")
                outfile.write(">" + taxon + "\n")
            else:
                outfile.write(line)
