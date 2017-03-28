# Improvements

## Before next release

### Bugs
+ Crashes at various steps if no sequences in one of the files

### Finish paper
+ ++ Find god damn benchmarking dataset
  - Use Victoria's but publish only subset?
+ Finish first draft
+ Add references
- Have Anaïs re-read it
- Have Louis re-read it
- Submit!

### Features
+ Include trimmomatic .jar file in `01_scripts/util`
+ Permit interleaved input

---

## Later

### Features
+ Decide if I can make a pre-formatted BOLD database available
- Add graphical representation of the pipeline for README.md and article
- Implement `natural_sort.py` for `08_summarize_read_dropout.sh`
- Support single-end data (no merge -> pseudo-merge script)
- Add de-interleave fastq script for single-file paired-end
- Add R script to produce read dropout figure and run from `01_scripts/08_...sh`

### Performance
- Blast only unique sequences for the whole dataset (v2.0)
  (big boost if lots of samples)
  - Create dictionary of unique reads
  - Blast them and store results
  - Assign results to each read of each pop
