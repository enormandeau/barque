# TODO

- Use commas (`,`) instead of tabs for `.csv` files
- Add `Sum` column to result `.csv`
- Improve code
  - Cleanup `08_summarize_read_dropout.sh`
  - Cleanup `09_get_most_frequent_non_annotated_sequences.sh`
  - `01_scripts/util/find_multiple_hits.sh` searches only for `.bold` files and does not report number
    of reads properly since we use unique reads
  - Make sure `01_scripts/util/missed_primers_01.sh` works with unique reads (should)
  - Remove need for uncompressed `.fasta` files in `07_split_amplicons`
  - Fix `09_get_most_frequent_non_annotated_sequences.sh` not working with unique reads
  - Provide alternative to merge for SE data
- Add config file for different scripts?
- Add graphical representation of the pipeline to README.md
- Provide detailed steps to run the pipeline in README.md

