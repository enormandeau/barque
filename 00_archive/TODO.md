# Version 1.6.0
- Re-organize documentation
  - keep it as short as possible
  - Describe how to create databases
  - Describe input sequence format requirements
    - file name
    - fastq and/or fastq.gz
  - Add commands in README.md to run test with test dataset
    - Clone test data
    - Copy in data folder
    - `time ./barque 02_info/barque.conf`

- Index databases only once (beginning of pipeline, with option to skip if existing)

# Maybe
- Create figures (amplicon split, multiple hits, read dropout)

# Potentially
- Perform de-noising before chimera removal (`--cluster_unoise`)
- Blast only unique sequences against reference (2X reduction only on medium dataset...)
  - Create dictionary of unique reads for all dataset (after chimeras)
  - Blast them and store results (sequence, hit)
  - Assign results to each read of each pop
- Support single-end data (no merge -> pseudo-merge script)
- Support interleaved input (flash can treat it)
