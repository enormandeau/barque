# Improvements

### Features

## Before next release
* Use vsearch for the blasts
  - Replace bold.udb by bold.fasta in scripts and test data folder

### Bugs
- Report real number of reads (not unique reads) affected by multiple hits

### Benchmarking
* Victoria's dataset (first 100k sequences per sample)
  - See benchmarking.xls

### Documentation
* Describe input sequence format requirements
  - file name
  - fastq and/or fastq.gz
+ Describe test dataset on `github.com/enormandeau/barque_test_dataset`
  - Include good `primers.csv` file

### Finish paper
- Finish first draft
- Add references

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
