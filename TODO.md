# Before 1.3

## Bugs
+ Confirm sequence lengths at each step
  - `07_split_by_amplicon.py` seems to keep reads that are too short (down to 61bp)

## Interface
- Improve messages for each step

## Documentation
- Describe input sequence format requirements
  - file name
  - fastq and/or fastq.gz
- Describe test dataset on `github.com/enormandeau/barque_test_dataset`
  - Include good `primers.csv` file

## Benchmarking
+ Victoria's dataset first 100k sequences per sample

## Finish paper
- Finish first draft
- Add references

-----------------------------------------------------------------------------

# Later

## Database formatting
- Revise bold formating scripts
  - Correctness
  - Possible to retain more sequences?
  - Shortest sequences at ~300bp. Too short?
- Make `bold.fasta.gz` available online

## Features
- Report real number of reads (not unique reads) affected by multiple hits
- R script to produce read dropout figure and run from `01_scripts/08_...sh`
- Support single-end data (no merge -> pseudo-merge script)
- Support interleaved input (flash can treat it)

## Performance
- Have 2 values for the number of CPUs:
  - For data preparation steps (read-write intensive)
  - For the vsearch steps (computation intensive)
- Blast only unique sequences for the whole dataset (v2.0)
  (big boost if lots of samples)
  - Create dictionary of unique reads
  - Blast them and store results
  - Assign results to each read of each pop
