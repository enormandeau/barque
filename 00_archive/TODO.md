# Roadmap for v1.5
## Features
* Treat taxon level (species, genus, phylum) in `07_summarize_results`
* Treat multiple hits in `07_summarize_results.py` directly
- Index databases only once (beginning of pipeline, with option to skip if existing)

## Bugs
- Number of reads are not sorted in the same order for different steps
  - Create a master script that does the summary

## Documentation
- Describe input sequence format requirements
  - file name
  - fastq and/or fastq.gz
- Describe test dataset on `github.com/enormandeau/barque_test_dataset`
  - Include good `primers.csv` file

# Later, maybe
- Blast only unique sequences
  - Create dictionary of unique reads for all dataset (after chimeras)
  - Blast them and store results (sequence, hit)
  - Assign results to each read of each pop
- Support single-end data (no merge -> pseudo-merge script)
- Support interleaved input (flash can treat it)
