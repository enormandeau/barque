# Version 1.6.0
- Stop producing following files:
  - multiple_hits_*
  - amplicon_split_summary.csv
  - chimera_sequences.fasta.gz

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
- Create read drop-out figure
