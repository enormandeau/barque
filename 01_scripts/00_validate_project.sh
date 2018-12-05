#!/bin/bash
# Validate project before launching Barque

# Global variables
DATABASE_FOLDER="03_databases"
DATA_FOLDER="04_data"

# Databases used in primers.csv file are present (.fasta.gz)
for database in $(cat 02_info/primers.csv | grep -v "^#" | cut -d "," -f 6)
do
    if ! [ -e "$DATABASE_FOLDER"/"$database".fasta -o -e "$DATABASE_FOLDER"/"$database".fasta.gz ]
    then
        echo -e "\n"BARQUE ERROR: Database file for \("$database"\) not found in "$DATABASE_FOLDER"
        echo Looking for "$DATABASE_FOLDER"/"$database"".fasta[.gz]"
        exit 1
    fi
done

# Data files (.fastq.gz or .fq.gz) are present in 04-data
if ! ls -1 "$DATA_FOLDER"/*.f*q.gz > /dev/null
then
    echo -e "\n"BARQUE ERROR: No sample found in "$DATA_FOLDER"
    exit 1
fi
