# BugFixes
- Sort num reads per step in similar way (lines that cross in dropouts)

# Features
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

# Performance
- Look for chimeras on per sample basis? As an option?
- Run `vsearch --usearch_global` in parallel
- Blast only unique sequences
  - Create dictionary of unique reads for all dataset
  - Blast them and store results (sequence, hit)
  - Assign results to each read of each pop
  - Big boost if lots of samples
  - Database will be read only once
