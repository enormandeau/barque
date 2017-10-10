# Roadmap for v1.5
## Features
* Treat multiple hits in `07_summarize_results.py` directly
- Blast only unique sequences
  - Create dictionary of unique reads for all dataset (after chimeras)
  - Blast them and store results (sequence, hit)
  - Assign results to each read of each pop

## Bugs
- Number of reads are not sorted in the same order for different steps

## Documentation
- Describe input sequence format requirements
  - file name
  - fastq and/or fastq.gz
- Describe test dataset on `github.com/enormandeau/barque_test_dataset`
  - Include good `primers.csv` file

# Later, maybe
- Support single-end data (no merge -> pseudo-merge script)
- Support interleaved input (flash can treat it)
