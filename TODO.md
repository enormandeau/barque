# TODO

## Bugs

## Features
* Use commas (`,`) instead of tabs for `.csv` files
* Add `Sum` column to result `.csv`
- Support single-end data (no merge -> pseudo-merge script)
- Add de-interleave fastq script for single-file paired-end
- Add config file for different scripts?

## Documentation
- Provide detailed steps to run the pipeline in README.md
- Add graphical representation of the pipeline to README.md

## Benchmark dataset
- Scripts and files to analyse benchmark data
  - SRA project file
  - primers.csv file
  - fastq-dump download script

## Performance
- Blast only unique sequences for the whole dataset
  (big boost if lots of samples)
  - Create dictionary of unique reads
  - Blast them and store results
  - Assign results to each read of each pop
