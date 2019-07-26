# Version 1.6.0
- Re-organize documentation
  - keep it as short as possible
  - Describe database format needed
  - Describe input sequence format requirements
    - Split by samples, tags removed but primers included
    - File name format
    - Format: fastq and/or fastq.gz
  
  - Add commands in README.md to run test with test dataset
    - Clone test data
    - Copy in data folder
    - `time ./barque 02_info/barque.conf`

- Index databases only once (beginning of pipeline, with option to skip if existing)

# Maybe
- Create read drop-out figure
