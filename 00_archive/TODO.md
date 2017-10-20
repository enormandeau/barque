# Version 1.6
## Features
- Index databases only once (beginning of pipeline, with option to skip if existing)

## Bugs
- Number of reads are not sorted in the same order for different steps
  - Create a master script that does the summary

# Later
## Features
- Use Genbank for annotation (create DB with efetch)
- Annotate reads then create OTUs and report on those too

## Documentation
- Describe input sequence format requirements
  - file name
  - fastq and/or fastq.gz
- Describe test dataset on `github.com/enormandeau/barque_test_dataset`
  - Include good `primers.csv` file

# Maybe
- Blast only unique sequences
  - Create dictionary of unique reads for all dataset (after chimeras)
  - Blast them and store results (sequence, hit)
  - Assign results to each read of each pop
- Support single-end data (no merge -> pseudo-merge script)
- Support interleaved input (flash can treat it)
