# Improvements

## Before next release
+ Rename folders so results are in last one (`15_results`?)

### Documentation
+ Describe input sequence format requirements
  - file name
  - fastq and/or fastq.gz
+ Describe test dataset on `github.com/enormandeau/barque_test_dataset`
  - Include good `primers.csv` file

### Benchmarking
- Victoria's dataset (first 100k sequences per sample)
  - See benchmarking.xls

### Finish paper
- Finish first draft
- Add references

---

## Later

### Database formatting
- Revise bold formating scripts
  - Correctness
  - Possible to retain more sequences?
  - Shortest sequences at ~300bp. Too short?
- Make `bold.fasta.gz` available online?

### Features
- Improve messages for each step
- Redirect full output to log folder with `tee`
- Report real number of reads (not unique reads) affected by multiple hits
- Add R script to produce read dropout figure and run from `01_scripts/08_...sh`
- Support single-end data (no merge -> pseudo-merge script)
- Support interleaved input (flash can treat it)
- Add graphical representation of the pipeline for README.md and article
- Implement `natural_sort.py` for `08_summarize_read_dropout.sh`

### Performance
- Have 2 values for the number of CPUs:
  - For data preparation steps (read-write intensive)
  - For the vsearch steps (computation intensive)
- Always treat biggest samples first in each step
- Find single-thread operations and parallelize them
- Blast only unique sequences for the whole dataset (v2.0)
  (big boost if lots of samples)
  - Create dictionary of unique reads
  - Blast them and store results
  - Assign results to each read of each pop
