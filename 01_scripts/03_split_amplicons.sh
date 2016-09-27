#!/bin/bash
ls -1 04_merged/*.fastq.gz | parallel ./01_scripts/split_amplicons_one_file.py 04_merged/{/} primers.csv iupac.csv 05_split_by_amplicon
