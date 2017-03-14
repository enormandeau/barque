# TODO

## Note
* Features with an asterix `*` need to be done before finishing the paper

## Bugs

## Features
* Add `Sum` column to result `.csv`
* Make compatible with Python 3
* Create launch script with all parameters in one place
* When and analysys is run, copy the exact script that was launched
* Add script to prepare database from bold and silva using parallel
* Add log info directory
* Support single-end data (no merge -> pseudo-merge script)
* Add de-interleave fastq script for single-file paired-end
- Add R script to procude read dropout figure and run from `01_scripts/08_...sh`

## Documentation
- Provide detailed steps to run the pipeline in README.md (or point to paper?)
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
