# Improvements

## Bugs
+ Fix hard coded path for trimmomatic
  - (?) Include .jar in `01_scripts/util`?

## Features
+ Add option to run only last portion of the analysis
  - after removing species from the database for example
+ (?) Make a pre-formatted BOLD database available somewhere as a .fasta file
- Support single-end data (no merge -> pseudo-merge script)
- Add de-interleave fastq script for single-file paired-end
- Add R script to produce read dropout figure and run from `01_scripts/08_...sh`

## Documentation
+ Add graphical representation of the pipeline to README.md

## Benchmark dataset
+ Choose test dataset and link to it or include it in Barque
  - (?) Use Victoria's?
+ Show how to run a small test
  - Move test dataset from `00_archive` to `04_data`
  - Move test dataset `primers.csv` to `02_info/primers.csv`
  - Get database (ideally with `wget`)
  - hit `.barque 02_info/barque_config.sh`

## Performance
- Blast only unique sequences for the whole dataset (v2.0)
  (big boost if lots of samples)
  - Create dictionary of unique reads
  - Blast them and store results
  - Assign results to each read of each pop
- Think about other ways to make the pipeline faster
