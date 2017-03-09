#!/bin/bash

# Find missed forward primers
zcat 07_split_amplicons/*not_found* | grep -E "^[ACTG]+$" | head -10000 | cut -c -20 | sort | uniq -c | sort -nr > forward_primers_not_found

# Find missed reverse primers
zcat 07_split_amplicons/*not_found* | grep -E "^[ACTG]+$" | head -10000 | grep -oE ".{20}$" | sort  | rev | tr "actgACTG" "tgacTGAC" | uniq -c | sort -nr > reverse_primers_not_found

# Edit files for missed_primers_02.py
vim -p forward_primers_not_found reverse_primers_not_found 02_info/primers.csv
