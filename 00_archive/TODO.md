# Roadmap for v1.4
## Features
- Validate project before launching Barque
  - Databases used in primers.csv file are present (.fasta.gz)
  - Data files (.fastq.gz or .fq.gz) are present in 04-data
  - Data files are properly named (sample name + "-")

- Run chimera search by sample
- Evalue cutoff for ncbi blasts

- Blast only unique sequences
  - Create dictionary of unique reads for all dataset (after chimeras)
  - Blast them and store results (sequence, hit)
  - Assign results to each read of each pop

## BugFixes
- Sort num reads per step in similar way (lines that cross in dropouts)

## Documentation
- Describe input sequence format requirements
  - file name
  - fastq and/or fastq.gz
- Describe test dataset on `github.com/enormandeau/barque_test_dataset`
  - Include good `primers.csv` file

# Later, maybe
- Support single-end data (no merge -> pseudo-merge script)
- Support interleaved input (flash can treat it)
