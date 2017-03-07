# Barque

### An environmental DNA metabarcoding analysis pipeline

![Barque](https://raw.githubusercontent.com/enormandeau/barque/master/00_archive/barque_small.png)

Developed by [Eric Normandeau](https://github.com/enormandeau) in
[Louis Bernatchez](http://www.bio.ulaval.ca/louisbernatchez/presentation.htm)'s
laboratory.

Please see licence information at the end of this file.

## TODO

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
- Add config file for different scripts?
- Improve README.md

## Short description

**Barque** was developped to analyze eDNA and metabarcoding datasets created
with COI and 18s sequences, although it could easily be extended to other
cases, as long as a database of amplified sequences exists for a comprehensive
set of species.

## Dependencies

**Barque** requires the following programs to be installed:

- python 2.7
- gnu parallel
- trimmomatic
- flash (read merger)
- usearch

## Overview

During the analyses, the following steps are performed:

- Get and format the database to usearch format (Python scripts, `usearch`)
- Filter and trim raw sequences (`trimmomatic`)
- Merge paired-end sequences (`flash`)
- Split sequence by amplicon (Python script)
- Merge all samples per amplicon (bash script)
- Find chimeras (`usearch -uchime_denovo`)
- Merge unique reads (Python script)
- Find species associated with each unique read (`usearch`)
- Summarize results (Python script)
  - Number of sequences per species per sample
  - Number of reads remaining at each analysis step
  - Output most frequent but non-annotated sequences for blast on NCBI nt/nr

## Running the pipeline

- TODO (step by step, including preparing `primers.csv` and the udb database)

## License
CC share-alike

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Barque</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Eric Normandeau</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/enormandeau/barque" rel="dct:source">https://github.com/enormandeau/barque</a>.
