# Improvements

## Before next release

### Bugs
+ Crashes at various steps if no sequences in one of the files

### Finish paper
+ Finish first draft
+ Add references

### Features
* Benchmark with Victoria's dataset (make available)
  - Full dataset
  - CPU number (1,2,4,8,16)
  - SSD vs. hard drive
  - Mermory usage
  - With and without chimera detection
  - Impact of dataset size?

### Documentation
* Describe input sequence format requirements
  - file name
  - fastq and/or fastq.gz

---

## Later

### Features
- Add graphical representation of the pipeline for README.md and article
- Implement `natural_sort.py` for `08_summarize_read_dropout.sh`
- Support single-end data (no merge -> pseudo-merge script)
- Support interleaved input (flash can treat it)
- Add R script to produce read dropout figure and run from `01_scripts/08_...sh`

### Performance
- Blast only unique sequences for the whole dataset (v2.0)
  (big boost if lots of samples)
  - Create dictionary of unique reads
  - Blast them and store results
  - Assign results to each read of each pop
