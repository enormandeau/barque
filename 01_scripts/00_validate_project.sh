#!/bin/bash
# Validate project before launching Barque

# Global variables
DATABASE_FOLDER="03_databases"
DATA_FOLDER="04_data"

# Permit only one primer pair per analysis
num_primers=$(grep -v "^#" 02_info/primers.csv | wc -l)

if [ "$num_primers" != 1 ]
then
    echo -e "\n"BARQUE ERROR: Specify exactly one primer pair in "02_info/primers.csv"
    exit 1
fi

# Databases used in primers.csv file are present (.fasta.gz)
for database in $(cat 02_info/primers.csv | grep -v "^#" | cut -d "," -f 6)
do
    if ! [ -e "$DATABASE_FOLDER"/"$database".fasta -o -e "$DATABASE_FOLDER"/"$database".fasta.gz ]
    then
        echo -e "\n"BARQUE ERROR: Database file for \("$database"\) not found in "$DATABASE_FOLDER"
        echo Looking for "$DATABASE_FOLDER"/"$database"".fasta[.gz]"
        exit 1

    else
        echo "- $database Database found"

    fi

done

# TODO
# Validate database format
# - Valid fasta format
# - Names are Family_Genus_species
# - Names optionally followed by a space and any kind of info on the same line

# Data files (.fastq.gz or .fq.gz) are present in 04-data
if ! ls -1 "$DATA_FOLDER"/*.f*q.gz > /dev/null
then
    echo -e "\n"BARQUE ERROR: No sample found in "$DATA_FOLDER"
    exit 1
fi

echo "-" $(ls -1 "$DATA_FOLDER"/*_R1*.f*q.gz | wc -l) "Samples found in $DATA_FOLDER"

# Function to compare version numbers
vercomp () {
    if [[ $1 == $2 ]]
    then
        return 0
    fi
    local IFS=.
    local i ver1=($1) ver2=($2)
    # fill empty fields in ver1 with zeros
    for ((i=${#ver1[@]}; i<${#ver2[@]}; i++))
    do
        ver1[i]=0
    done
    for ((i=0; i<${#ver1[@]}; i++))
    do
        if [[ -z ${ver2[i]} ]]
        then
            # fill empty fields in ver2 with zeros
            ver2[i]=0
        fi
        if ((10#${ver1[i]} > 10#${ver2[i]}))
        then
            return 1
        fi
        if ((10#${ver1[i]} < 10#${ver2[i]}))
        then
            return 2
        fi
    done
    return 0
}

# Validate that vsearch is installed
command -v vsearch >/dev/null 2>&1 ||
    {
        echo -e "\n"BARQUE ERROR: vsearch is not installed
        echo
        exit 1;
    }

# Confirm that vsearch version is high enough
vsearch_needed="2.14.2"
vsearch_version=$(vsearch --version 2>&1 | head -1 | awk '{print $2}' | cut -d "_" -f 1 | perl -pe 's/^v//')

vercomp "$vsearch_version" "$vsearch_needed"

case $? in
    0)
        echo "- vsearch is recent enough:"
        echo "    needed: $vsearch_needed""+; installed: $vsearch_version";;
    1)
        echo "- vsearch is recent enough:"
        echo "    needed: $vsearch_needed""+; installed: $vsearch_version";;
    2)
        echo
        echo "/!\ WARNING /!\ "
        echo
        echo "vsearch ($vsearch_version) is too old"
        echo "You need version $vsearch_needed""+ to run Barque"
        echo
        echo ">>> STOPPING BARQUE <<<"
        echo
        exit 1;;
esac

# Validate that python3 is installed and used
command -v python3 >/dev/null 2>&1 ||
    {
        echo -e "\n"BARQUE ERROR: python3 is not installed
        echo
        exit 1;
    }

# Confirm that python3 version is high enough
python3_needed="3.5.0"
python3_version=$(python3 --version 2>&1 | head -1 | awk '{print $2}')

vercomp "$python3_version" "$python3_needed"

case $? in
    0)
        echo "- python3 is recent enough:"
        echo "    needed: $python3_needed""+; installed: $python3_version";;
    1)
        echo "- python3 is recent enough:"
        echo "    needed: $python3_needed""+; installed: $python3_version";;
    2)
        echo
        echo "/!\ WARNING /!\ "
        echo
        echo "python3 ($python3_version) is too old"
        echo "You need version $python3_needed""+ to run Barque"
        echo
        echo ">>> STOPPING BARQUE <<<"
        echo
        exit 1;;
esac

# Validate that java is installed and used
command -v java >/dev/null 2>&1 ||
    {
        echo -e "\n"BARQUE ERROR: java is not installed
        echo
        exit 1;
    }

# Validate that R is installed and used
command -v R >/dev/null 2>&1 ||
    {
        echo -e "\n"BARQUE ERROR: R is not installed
        echo
        exit 1;
    }

# Confirm that R version is high enough
R_needed="3.0.0"
R_version=$(R --version 2>&1 | head -1 | awk '{print $3}')

vercomp "$R_version" "$R_needed"

case $? in
    0)
        echo "- R is recent enough:"
        echo "    needed: $R_needed""+; installed: $R_version";;
    1)
        echo "- R is recent enough:"
        echo "    needed: $R_needed""+; installed: $R_version";;
    2)
        echo
        echo "/!\ WARNING /!\ "
        echo
        echo "R ($R_version) is too old"
        echo "You need version $R_needed""+ to run Barque"
        echo
        echo ">>> STOPPING BARQUE <<<"
        echo
        exit 1;;
esac

# Validate that parallel is installed and used
command -v parallel --version >/dev/null 2>&1 ||
    {
        echo -e "\n"BARQUE ERROR: parallel is not installed
        echo
        exit 1;
    }

# Confirm that parallel version is high enough
parallel_needed="20180101"
parallel_version=$(parallel --version 2>&1 | head -1 | awk '{print $3}')

vercomp "$parallel_version" "$parallel_needed"

case $? in
    0)
        echo "- parallel is recent enough:"
        echo "    needed: $parallel_needed""+; installed: $parallel_version";;
    1)
        echo "- parallel is recent enough:"
        echo "    needed: $parallel_needed""+; installed: $parallel_version";;
    2)
        echo
        echo "/!\ WARNING /!\ "
        echo
        echo "parallel ($parallel_version) is too old"
        echo "You need version $parallel_needed""+ to run Barque"
        echo
        echo ">>> STOPPING BARQUE <<<"
        echo
        exit 1;;
esac

# Validate that flash is installed
command -v flash --version >/dev/null 2>&1 ||
    {
        echo -e "\n"BARQUE ERROR: flash is not installed
        echo
        exit 1;
    }

# Confirm that flash version is high enough
flash_needed="1.2.11"
flash_version=$(flash --version 2>&1 | head -1 | awk '{print $2}' | cut -d "_" -f 1 | perl -pe 's/^v//')

vercomp "$flash_version" "$flash_needed"

case $? in
    0)
        echo "- flash is recent enough:"
        echo "    needed: $flash_needed""+; installed: $flash_version";;
    1)
        echo "- flash is recent enough:"
        echo "    needed: $flash_needed""+; installed: $flash_version";;
    2)
        echo
        echo "/!\ WARNING /!\ "
        echo
        echo "flash ($flash_version) is too old"
        echo "You need version $flash_needed""+ to run Barque"
        echo
        echo ">>> STOPPING BARQUE <<<"
        echo
        exit 1;;
esac
