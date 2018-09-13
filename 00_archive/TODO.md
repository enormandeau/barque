# Next minor version
- Improve script for splitting by primers (this is where we lose the most reads with 12S)
- Remove temp results files in folders 05 to 11 when they are no longer needed

# Version 1.5.x
- Index databases only once (beginning of pipeline, with option to skip if existing)
- Perform de-noising before chimera removal (`--cluster_unoise`) ?
- Describe input sequence format requirements
  - file name
  - fastq and/or fastq.gz
- Describe test dataset on `github.com/enormandeau/barque_test_dataset`
  - Include good `primers.csv` file
- Add commands in README.md to run test with test dataset
  - Clone test data
  - Copy in data folder
  - `time ./barque 02_info/barque.conf`
- Number of reads are not sorted in the same order for different steps
  - Create a master script that does the summary

# Maybe
- Create figures (amplicon split, multiple hits, read dropout)
- Blast only unique sequences
  - Create dictionary of unique reads for all dataset (after chimeras)
  - Blast them and store results (sequence, hit)
  - Assign results to each read of each pop
- Support single-end data (no merge -> pseudo-merge script)
- Support interleaved input (flash can treat it)
