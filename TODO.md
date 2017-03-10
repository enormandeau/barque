# TODO

## Note
* Features with an asterix `*` need to be done before finishing the paper

## Bugs

## Features
* **Add script to prepare database from bold and silva using parallel**
* Replace `.tsv` files with `.csv` files
* Use commas (`,`) instead of tabs for `.csv` files
* Add `Sum` column to result `.csv`
* Make compatible with Python 3
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
- Blast only unique sequences for the whole dataset (v2.0)
  (big boost if lots of samples)
  - Create dictionary of unique reads
  - Blast them and store results
  - Assign results to each read of each pop
- Think about other ways to make the pipeline faster
