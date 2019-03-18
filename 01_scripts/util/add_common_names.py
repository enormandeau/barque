#!/usr/bin/env python3
"""Add common species name to species_table.csv

Usage:
    <program> species_table_file common_names_file output_file

Where:
    species_table_file is the output from Barque
    output_file has the same format but with an added column
    common_names_file has the following format:

Family         Genus      Species     Taxon_name                          Common_name
Acipenseridae  Acipenser  fulvescens  Acipenseridae Acipenser fulvescens  Esturgeon jaune
Acipenseridae  Acipenser  oxyrinchus  Acipenseridae Acipenser oxyrinchus  Esturgeon noir
Amiidae        Amia       calva       Amiidae Amia calva                  Poisson-castor
Ammodytidae    Ammodytes  americanus  Ammodytidae Ammodytes americanus    Laon d'Amérique
Ammodytidae    Ammodytes  dubius      Ammodytidae Ammodytes dubius        Laon du nord
Ammodytidae    Ammodytes  hexapterus  Ammodytidae Ammodytes hexapterus    Laon gourdeau
Ammodytidae    Ammodytes  personatus  Ammodytidae Ammodytes personatus    Laon du Pacifique
Anguillidae    Anguilla   rostrata    Anguillidae Anguilla rostrata       Anguille d'Amérique
"""

# Modules
import sys

# Parsing user input
try:
    species_table_file = sys.argv[1]
    common_names_file = sys.argv[2]
    output_file = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Load common names
common_names = dict()
common_names["TaxonName"] = "CommonName"

with open(common_names_file) as infile:
    for line in infile:
        l = line.strip().split("\t")
        family, genus, species, taxon, common = l
        common_names[taxon] = common

# Add common names to species_table
with open(species_table_file) as infile:
    with open(output_file, "w") as outfile:
        for line in infile:
            l = line.strip().split(",")

            try:
                common = common_names[l[3]]

            except KeyError:
                common = "na"

            new_line = l[:4] + [common] + l[4:]
            outfile.write(",".join(new_line) + "\n")
