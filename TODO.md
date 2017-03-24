# Improvements

## Before next release

### Features
- (...) Fix hard coded path for trimmomatic (Include .jar in `01_scripts/util`?)
- (...) Make a pre-formatted BOLD database available somewhere as a .fasta file

---

## Later

### Features
- Add graphical representation of the pipeline for README.md and article
- Implement `natural_sort.py` for `08_summarize_read_dropout.sh`
- Support single-end data (no merge -> pseudo-merge script)
- Add de-interleave fastq script for single-file paired-end
- Add R script to produce read dropout figure and run from `01_scripts/08_...sh`
- Create a GitHub repo Wiki page?

### Performance
- Blast only unique sequences for the whole dataset (v2.0)
  (big boost if lots of samples)
  - Create dictionary of unique reads
  - Blast them and store results
  - Assign results to each read of each pop
