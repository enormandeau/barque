# TODO

## Documentation

- Provide detailed steps to run the pipeline in README.md
- Add graphical representation of the pipeline to README.md

## Features

- Scripts and files to analyse benchmark data
  - SRA project file
  - primers.csv file
  - fastq-dump download script
  - de-interleave fastq script
- Use commas (`,`) instead of tabs for `.csv` files
- Add `Sum` column to result `.csv`
- Add config file for different scripts?
- Support single-end data (no merge -> pseudo-merge script)

## Performance
- Blast only unique sequences for the whole dataset
  (big boost if lots of samples)

## Improving code

- Cleanup `08_summarize_read_dropout.sh`
- `01_scripts/util/find_multiple_hits.sh` searches only for `.bold` files and
  does not report number of reads properly since we use unique reads
- Make sure `01_scripts/util/missed_primers_01.sh` works with unique reads
- Remove need for uncompressed `.fasta` files in `07_split_amplicons`
