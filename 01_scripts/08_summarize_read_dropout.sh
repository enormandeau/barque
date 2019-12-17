#!/bin/bash
# Show number of reads per sample through pipeline

# 04_data
step="04_data"
cd "$step"
echo -e "Sample,$step" > ../10_read_dropout/$step
for i in *R1_001.fastq.gz
do
    echo -e $(echo "$i" | cut -d "_" -f 1)","$(echo $(gunzip -c "$i" | wc -l) / 4 | bc | cut -d "." -f 1)
done | sort -t "," -k1,1 -V >> ../10_read_dropout/$step
cd ..

# 05_trimmed
step="05_trimmed"
cd "$step"
echo -e "$step" > ../10_read_dropout/$step
for i in *R1_001.fastq.gz
do
    echo -e $(echo "$i" | cut -d "_" -f 1)","$(echo $(gunzip -c "$i" | wc -l) / 4 | bc | cut -d "." -f 1)
done | sort -t "," -k1,1 -V | cut -d "," -f 2 >> ../10_read_dropout/$step
cd ..

# 06_merged
step="06_merged"
cd "$step"
echo -e "$step" > ../10_read_dropout/$step
for i in *.gz
do
    echo -e $(echo "$i" | cut -d "_" -f 1)","$(echo $(gunzip -c "$i" | wc -l) / 4 | bc | cut -d "." -f 1)
done | sort -t "," -k1,1 -V | cut -d "," -f 2 >> ../10_read_dropout/$step
cd ..

# 07_split_amplicons
step="07_split_amplicons"
cd "$step"
for i in $(grep -v "^#" ../02_info/primers.csv | awk -F "," '{print $1}')
do
    echo -e "$step" > ../10_read_dropout/"$step"_"$i"
    for j in $(ls -1 *merged_"$i"*.gz | grep "$i")
    do
        echo -e $(echo "$j" | cut -d "_" -f 1)","$(echo $(gunzip -c "$j" | wc -l) / 4 | bc | cut -d "." -f 1)
    done | sort -t "," -k1,1 -V | cut -d "," -f 2 >> ../10_read_dropout/"$step"_"$i"
done
cd ..

# 08_chimeras
step="08_chimeras"
cd "$step"
for i in $(grep -v "^#" ../02_info/primers.csv | awk -F "," '{print $1}')
do
    echo -e "$step" > ../10_read_dropout/"$step"_"$i"
    for j in $(ls -1 *merged_"$i"*_unique.fasta.gz | grep "$i")
    do
        echo -e $(echo "$j" | cut -d "_" -f 1)","$(echo $(gunzip -c "$j" | grep ">" | cut -d "_" -f 4 | awk '{s+=$1}END{print s}'))
    done | sort -t "," -k1,1 -V | cut -d "," -f 2 >> ../10_read_dropout/"$step"_"$i"
done
cd ..

# 12_results
step="12_results"
cd "$step"
for i in $(grep -v "^#" ../02_info/primers.csv | awk -F "," '{print $1}')
do
    echo -e "$step" > ../10_read_dropout/"$step"_"$i"; awk -F "," 'NR==1 {for (i=1; i<=NF; i++) {headers[i]=$i}} NR>1 {for (i=1; i<=NF; i++) {sums[i]+=$i}} END {for (i=6; i<=NF; i++) {print headers[i]","sums[i]}}' "$i"_species_table.csv | sort -t "," -k1,1 -V | cut -d "," -f 2 >> ../10_read_dropout/"$step"_"$i"
done
cd ..

# Put everything together
step="10_read_dropout"
cd "$step"
paste -d "," 04_data 05_trimmed 06_merged 07_split_amplicons_* 08_chimeras_* 12_results* > ../12_results/sequence_dropout.csv
cd ..
