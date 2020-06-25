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

    else
        echo "- $database Database found"

    fi

done

# Data files (.fastq.gz or .fq.gz) are present in 04-data
if ! ls -1 "$DATA_FOLDER"/*.f*q.gz > /dev/null
then
    echo -e "\n"BARQUE ERROR: No sample found in "$DATA_FOLDER"
    exit 1
fi

echo "-" $(ls -1 "$DATA_FOLDER"/*_R1_*.f*q.gz | wc -l) "Samples found in $DATA_FOLDER"

# Validate that vsearch is v2.14.2+
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
