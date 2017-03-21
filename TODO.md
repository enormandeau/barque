# TODO

## Bugs

## Features
+ Regroup all results in one folder with date and the name of the config file?
+ Make it possible to run the separate scripts (source the config file in each .sh file?)
+ Add script to prepare database from bold and silva using parallel
  (host prepared libraries somewhere?)
- Support single-end data (no merge -> pseudo-merge script)
- Add de-interleave fastq script for single-file paired-end
- Add R script to produce read dropout figure and run from `01_scripts/08_...sh`

## Documentation
+ Provide detailed steps to run the pipeline in README.md (or point to paper?)
  - Fill the config file
  - Run `barque`
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
