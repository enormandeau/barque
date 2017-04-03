# Barque v1.3

## An environmental DNA metabarcoding analysis pipeline

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
- [gnu parallel](https://www.gnu.org/software/parallel/)
- [flash (read merger)](https://sourceforge.net/projects/flashpage/)
- [vsearch](https://github.com/torognes/vsearch)

## Preparation
- Install dependencies
- Download **Barque** (see **Installation** section above)
- Get database and format it (Python scripts)
- Edit `02_info/primers.csv`
- Make a copy of `02_info/barque_config.sh` and edit the parameters

## Analyses

During the analyses, the following steps are performed:

- Filter and trim raw reads (`trimmomatic`)
- Merge paired-end reads (`flash`)
- Split merged reads by amplicon (Python script)
- Look for chimeras (optional, `vsearch --vsearch_global`)
- Merge unique reads (Python script)
- Find species associated with each unique read (`vsearch`)
- Summarize results (Python script)
  - Tables of phylum, genus, and species counts per sample
  - Chimera sequences
  - Cases of multiple hits with equal scores
  - Number of reads remaining at each analysis step
  - Most frequent non-annotated sequences to blast on NCBI nt/nr
  - Species counts for these non-annotated sequences

## Lather, Rince, Repeat

Once the pipeline has been run, it is normal to find that unexpected species
have been found or that a proportion of the reads have not been identified
using the database. In these cases, you will need to create a list of unwanted
species to be later removed from the database or download additional sequences
for the non-annotated species from NCBI to add them to the database. Once the
database has been improved, simply run the last part of the pipeline by making
sure you have `SKIP_DATA_PREP=0` in your config file. You may need to repeat
this step again until you are satisfied with the results.

NOTE: You should provide justifications in your publications explaining why you
decided to remove some species from the database.

## Running the pipeline

For each new project, get a new copy of **Barque** from the sources listed in
the **Installation** section and copy your data in the `04_data` folder. You
will also need to put a database in Fasta format (usually `bold.fasta`) in the
`03_databases` folder.

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
The pipeline must then be re-run from the `vsearch` scripts
(`./01_scripts/06_vsearch_multiple_hits.sh` and `./01_scripts/06_vsearch.sh`).

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

#TODO update this part
```bash
./01_scripts/10_report_species_for_non_annotated_sequences.py \
    12_results/NCBI-Alignment.txt \
    most_frequent_non_annotated_sequences_species_ncbi.csv
```

## Test dataset

A test dataset and corresponding `primers.csv` file is available as a
[sister repository on GitHub](https://github.com/enormandeau/barque_test_dataset).
Download the repository and then move the data in **Barque**'s `04_data` folder
and the `primers.csv` file in the `02_info` folder. Follow the normal pipeline
procedure (including database preparation) to analyse this small dataset. it
should run in one to ten minutes depending on your computer.

## Citation

When using **Barque**, please cite the following paper:

- TODO Add citation information and link to paper

## License

CC share-alike

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Barque</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Eric Normandeau</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/enormandeau/barque" rel="dct:source">https://github.com/enormandeau/barque</a>.
