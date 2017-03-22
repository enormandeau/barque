# Barque

## Version 1.3

### An environmental DNA metabarcoding analysis pipeline

![Barque](https://raw.githubusercontent.com/enormandeau/barque/master/00_archive/barque_small.png)

Developed by [Eric Normandeau](https://github.com/enormandeau) in
[Louis Bernatchez](http://www.bio.ulaval.ca/louisbernatchez/presentation.htm)'s
laboratory.

Please see licence information at the end of this file.

## Description

**Barque** is a metabarcoding dataset analysis pipeline that relies on high
quality metabarcoding databases instead of the generation of operational
taxonomic unit (OTUs). It is parallelized, fast, and streamlined. It uses
well-tested programs and is compatible with both Python 2 and 3.

## Use cases

The approaches implemented in **Barque** is especially useful for species
management projects:

- Large spectrum monitoring of invasive species
- Confirming the presence of specific species
- Improve species distribution knowledge of cryptic taxa
- Characterizing meta-communities in varied environments
- Loss of species over medium to long-term monitoring

Since it depends on the use of high quality metabarcoding databases, it is
especially useful for COI amplicons used in combination with the Barcode of
Life Database (BOLD).

## Installation

To use **Barque**, you will need a local copy of its repository, which can be
[found here](https://github.com/enormandeau/barque/archive/master.zip). Different releases can be
[accessed here](https://github.com/enormandeau/barque/releases). It is
recommended to use the latest version or at least version 1.3.

## Dependencies

You will also need to have the following programs installed on your computer.

- bash 4+
- python 2.7+ or 3.5+
- fastq-dump from sra-toolkit to download the benchmark dataset
- gnu parallel
- trimmomatic
- flash (read merger)
- usearch

## Overview

During the analyses, the following steps are performed:

- Get databases and format them to the usearch format (Python scripts, `usearch`)
- Filter and trim raw reads (`trimmomatic`)
- Merge paired-end reads (`flash`)
- Split merged reads by amplicon (Python script)
- Merge all samples per amplicon (bash script)
- Look for chimeras (optional, `usearch -uchime_denovo`)
- Merge unique reads (Python script)
- Find species associated with each unique read (`usearch`)
- Summarize results (Python script)
  - Cases of multiple hits with equal scores
  - Number of sequences per species per sample
  - Number of reads remaining at each analysis step
  - Output most frequent but non-annotated sequences for blast on NCBI nt/nr

## Running the pipeline

To run **Barque**, make a copy of the file named `02_info/barque_config.sh` and
modify the parameters as needed, then launch the `barque` executable with the
name of your configuration file as an argument, like this:
```
./barque 02_info/MY_CONFIG_FILE.sh
```

## Results

Once the pipeline has run, all result files are found in the `12_results`
folder.

### Taxa count tables, named after the primer names

- `PRIMER_phylum_table.csv`
- `PRIMER_genus_table.csv`
- `PRIMER_species_table.csv`

### Chimeras

- `all_PRIMER.fasta.unique.chimeras`. No chimera detected if this file is empty.

### Information about sequences with multiple hits of equal score

- `multiple_hits.txt`: This file is divided into groups of species. For each
groups, the number at the top, listed as `N times(s)`, indicates how many
unique sequences (which may represent a higher number of sequences) had equal
quality scores when aligned to sequences of all the species in the group. It is
worth going through this file and identify species that are very unlikely in
the area where the samples were taken. These samples can then be added to a
`species_to_remove.txt` file and the database can be filtered to remove them.
The database then needs to be re-indexed for use with `usearch` and the
pipeline must be re-run from the `usearch` scripts
(`./01_scripts/06_usearch_multiple_hits.sh` and `./01_scripts/06_usearch.sh`).

### Sequence dropout report

- `sequence_dropout.csv`: Listing how many sequences were present in each
sample for every analysis step.

## Citation

When using **Barque**, please cite the following paper:

- TODO Add citation information and link to paper

## License

CC share-alike

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Barque</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Eric Normandeau</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/enormandeau/barque" rel="dct:source">https://github.com/enormandeau/barque</a>.
