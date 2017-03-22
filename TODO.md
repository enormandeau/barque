# Improvements

## Bugs

## Features
+ Add script to prepare database from bold and silva using parallel
  (host prepared libraries somewhere?)
+ Make a pre-formatted BOLD database available somewhere as a .fasta file?
- Support single-end data (no merge -> pseudo-merge script)
- Add de-interleave fastq script for single-file paired-end
- Add R script to produce read dropout figure and run from `01_scripts/08_...sh`

## Documentation
+ Add graphical representation of the pipeline to README.md

## Benchmark dataset
- Scripts and files to analyse benchmark data
  - SRA project file
  - primers.csv file
  - fastq-dump download script

## Performance
- Blast only unique sequences for the whole dataset (v2.0)
  (big boost if lots of samples)
  - Create dictionary of unique reads
  - Blast them and store results
  - Assign results to each read of each pop
- Think about other ways to make the pipeline faster
