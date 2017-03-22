#!/bin/bash
# Show number of reads per sample through pipelin

# 04_data
step="04_data"
cd "$step"
echo -e "Sample,$step" > ../13_read_dropout/$step
for i in *R1*.gz
do
    echo -e $(echo "$i" | cut -d "_" -f 1)","$(echo $(gunzip -c "$i" | wc -l) / 4 | bc | cut -d "." -f 1)
done | sort -V >> ../13_read_dropout/$step
cd ..

# 05_trimmed
step="05_trimmed"
cd "$step"
echo -e "$step" > ../13_read_dropout/$step
for i in *R1*.gz
do
    echo -e $(echo "$i" | cut -d "_" -f 1)"\t"$(echo $(gunzip -c "$i" | wc -l) / 4 | bc | cut -d "." -f 1)
done | sort -V | awk '{print $2}' >> ../13_read_dropout/$step
cd ..

# 06_merged
step="06_merged"
cd "$step"
echo -e "$step" > ../13_read_dropout/$step
for i in *.gz
do
    echo -e $(echo "$i" | cut -d "_" -f 1)"\t"$(echo $(gunzip -c "$i" | wc -l) / 4 | bc | cut -d "." -f 1)
done | sort -V | awk '{print $2}' >> ../13_read_dropout/$step
cd ..

# 07_split_amplicons
step="07_split_amplicons"
cd "$step"
for i in $(grep -v "^#" ../02_info/primers.csv | awk -F "," '{print $1}')
do
    echo -e "$step" > ../13_read_dropout/"$step"_"$i"
    for j in $(ls -1 *merged_"$i"*.gz | grep "$i")
    do
        echo -e $(echo "$j" | cut -d "_" -f 1)"\t"$(echo $(gunzip -c "$j" | wc -l) / 4 | bc | cut -d "." -f 1)
    done | sort -V | awk '{print $2}' >> ../13_read_dropout/"$step"_"$i"
done
cd ..

# 12_results
step="12_results"
cd "$step"
for i in $(grep -v "^#" ../02_info/primers.csv | awk -F "," '{print $1}')
do
    echo -e "$step" > ../13_read_dropout/"$step"_"$i"; awk -F "," 'NR==1 {for (i=1; i<=NF; i++) {headers[i]=$i}} NR>1 {for (i=1; i<=NF; i++) {sums[i]+=$i}} END {for (i=5; i<=NF; i++) {print headers[i]"\t"sums[i]}}' "$i"_species_table.csv | sort -V | awk '{print $2}' >> ../13_read_dropout/"$step"_"$i"
done
cd ..

# Put everything together
step="13_read_dropout"
cd "$step"
paste -d "," 04_data 05_trimmed 06_merged 07_split_amplicons_* 12_results_* > ../12_results/sequence_dropout.csv
cd ..
