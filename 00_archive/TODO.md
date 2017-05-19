# Features
- Remove sequences with multiple hits from results
  - If impossible species are removed, this should bring most of them back
- Validate project before launching Barque
  - Databases used in primers.csv file are present (.fasta.gz)
  - Data files (.fastq.gz or .fq.gz) are present in 04-data
  - Data files are properly named (sample name + "-")
- Support single-end data (no merge -> pseudo-merge script)
- Support interleaved input (flash can treat it)

# Documentation
- Describe input sequence format requirements
  - file name
  - fastq and/or fastq.gz
- Describe test dataset on `github.com/enormandeau/barque_test_dataset`
  - Include good `primers.csv` file

---

# Benchmarking
- Victoria's dataset first 100k sequences per sample
  - Find way to get time plus CPU and memory usage through time

# Paper
- Finish first draft
- Add references

---

# Performance
- Look for chimeras on _per sample_ basis?
- Run `vsearch --usearch_global` in parallel
- Blast only unique sequences
  - Create dictionary of unique reads for all dataset
  - Blast them and store results (sequence, hit)
  - Assign results to each read of each pop
  - Big boost if lots of samples
  - Database will be read only once
