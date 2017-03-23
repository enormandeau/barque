# Barque

## Version 1.3

### An environmental DNA metabarcoding analysis pipeline

![Barque](https://raw.githubusercontent.com/enormandeau/barque/master/00_archive/barque_small.png)

Developed by [Eric Normandeau](https://github.com/enormandeau) in
[Louis Bernatchez](http://www.bio.ulaval.ca/louisbernatchez/presentation.htm)'s
laboratory.

Please see citation and licence information at the end of this file.

## Documentation

This documentation file can be
[found here](https://github.com/enormandeau/barque/blob/master/README.md).

## Description

**Barque** is a metabarcoding analysis pipeline that relies on high quality
metabarcoding-specific databases instead of generating Operational Taxonomic
Unit (OTUs). It is parallelized, fast, and streamlined. It uses well-tested
programs and is compatible with both Python 2 and 3.

## Use cases

The approach implemented in **Barque** is especially useful for species
management projects:

- Monitoring of invasive species
- Confirming the presence of specific species
- Characterizing meta-communities in varied environments
- Improving species distribution knowledge for cryptic taxa
- Following loss of species over medium to long-term monitoring

Since it depends on the use of high quality metabarcoding databases, it is
especially useful for COI amplicons used in combination with the Barcode of
Life Database (BOLD), although it can also use other databases like Silva.

## Installation

To use **Barque**, you will need a local copy of its repository, which can be
[found here](https://github.com/enormandeau/barque/archive/master.zip).
Different releases can be
[accessed here](https://github.com/enormandeau/barque/releases). It is
recommended to use the latest version or at least version 1.3.

## Dependencies

You will also need to have the following programs installed on your computer.

- OSX or GNU Linux
- bash 4+
- python 2.7+ or 3.5+
- gnu parallel
- flash (read merger)
- usearch
- *REMOVE*? trimmomatic

## Overview

During the analyses, the following steps are performed:

- Get database and index with usearch (Python scripts, `usearch`)
- Filter and trim raw reads (`trimmomatic`)
- Merge paired-end reads (`flash`)
- Split merged reads by amplicon (Python script)
- Merge all samples per amplicon (bash script)
- Look for chimeras (optional, `usearch -uchime_denovo`)
- Merge unique reads (Python script)
- Find species associated with each unique read (`usearch`)
- Summarize results (Python script)
  - Tables of phylum, genus, and species counts per sample
  - Chimera sequences
  - Cases of multiple hits with equal scores
  - Number of reads remaining at each analysis step
  - Output most frequent but non-annotated sequences to blast on NCBI nt/nr

## Running the pipeline

For each new project, get a new copy of **Barque** from the sources listed in
the **Installation** section and copy your data in the `04_data` folder. You
will also need to put a usearch-indexed database (usually `bold.udb`) in
the `03_databases` folder.

If you do not already have the indexed database and want to use BOLD, you will
need to download all the animal BINs from
[this BOLD page](http://www.boldsystems.org/index.php/Public_BarcodeIndexNumber_Home).
Put the downloaded Fasta files in `03_databases/bold_bins` (you may need to
create that folder), and run the commands to format the bold database:

```bash
# Format each BIN individually (~10 minutes)
# Note: the `species_to_remove.txt` file is optional
ls -1 03_databases/bold_bins/*.fas.gz |
    parallel ./01_scripts/util/format_bold_database.py \
    {} {.}_prepared.fasta.gz species_to_remove.txt

# Concatenate the resulting formatted bins into one file (~10 seconds)
gunzip -c 03_databases/bold_bins/*_prepared.fasta.gz > 03_databases/bold.fasta

# Index the BOLD database for usearch (~20 seconds)
usearch -makeudb_usearch 03_databases/bold.fasta -output 03_databases/bold.udb
```

Make a copy of the file named `02_info/barque_config.sh` and modify the
parameters as needed, then launch the `barque` executable with the name of your
configuration file as an argument, like this:

```bash
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

- `chimera_PRIMER.fasta.unique.chimeras`. No chimera detected if this file is empty.

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
sample for every analysis step. Depending on library and sequencing quality, as
well as the biological diversity found at the sample site, more or less
sequences are lost at each of the analysis steps.

### Most frequent bun non-annotated sequences

- `most_frequent_non_annotated_sequences.fasta`: Sequences that are frequent
in the samples but were not annotated by the pipeline. This Fasta file should be
used to query the NCBI nt/nr database using the online portal
[found here](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastSearch)
to see what species may have been missed. Use `blastn` with default parameters.
Once the NCBI blastn search is finished, download the results as a text file
and use the following command (you will need to adjust the input and output
file names) to generate a report of the most frequently found species in the
non-annotated sequences:

```bash
./01_scripts/10_report_species_for_non_annotated_sequences.py 12_results/NCBI-Alignment.txt most_frequent_non_annotated_sequences_species_ncbi.csv
```

## Citation

When using **Barque**, please cite the following paper:

- TODO Add citation information and link to paper

## License

CC share-alike

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Barque</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Eric Normandeau</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/enormandeau/barque" rel="dct:source">https://github.com/enormandeau/barque</a>.
