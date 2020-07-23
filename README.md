# Barque v1.6.3

## Environmental DNA metabarcoding analysis

![Barque](https://raw.githubusercontent.com/enormandeau/barque/master/00_archive/barque_small.png)

Developed by [Eric Normandeau](https://github.com/enormandeau) in
[Louis Bernatchez](http://www.bio.ulaval.ca/louisbernatchez/presentation.htm)'s
laboratory.

See licence information at the end of this file.

## Description

**Barque** is an eDNA metabarcoding analysis pipeline that annotates reads,
instead of Operational Taxonomic Unit (OTUs), using high-quality barcoding
databases.

**Barque** can also produce OTUs, which are then annotated using a database.
These annotated OTUs are used as a database to find read counts per OTU per
sample.

## Use cases

The approach implemented in **Barque** is especially useful for species
management projects:

- Monitoring of invasive species
- Confirming the presence of specific species
- Characterizing meta-communities in varied environments
- Improving species distribution knowledge for cryptic taxa
- Following loss of species over medium to long-term monitoring

Since Barque depends on the use of high-quality barcoding databases, it is
especially useful for COI amplicons used in combination with the Barcode of
Life Database (BOLD) or 12S amplicons with the mitofish database, although it
can also use any database, for example the Silva database for the 18s gene or
any other custom database.

## Installation

To use **Barque**, you will need a local copy of its repository. Different
releases can be [accessed
here](https://github.com/enormandeau/barque/releases). It is recommended to
use the latest version.

### Dependencies

To run **Barque**, you will also need to have the following programs installed
on your computer.

- **Barque** will only work on GNU Linux or OSX
- bash 4+
- python 3.5+ (you can use miniconda)
- R 3+ (ubuntu/mint: `sudo apt-get install r-base-core`)
- java (ubuntu/mint: `sudo apt-get install default-jre`)
- [gnu parallel](https://www.gnu.org/software/parallel/)
- [flash (read merger)](https://ccb.jhu.edu/software/FLASH/) v1.2.11+
- [vsearch](https://github.com/torognes/vsearch/releases) v2.14.2+
  - /!\ **v2.14.2+ required** /!\
  - **Barque will not work with older versions of vsearch**

### Preparation

- Install dependencies
- Download a copy of the **Barque** repository (see **Installation** section above)
- Get or prepare the database(s) (see Formatting database section below)
- Edit `02_info/primers.csv` to provide needed informations for your primers
- Make a copy of `02_info/barque_config.sh` and modify the parameters for your run
- Launch Barque

## Overview of Barque steps

During the analyses, the following steps are performed:

- Filter and trim raw reads (`trimmomatic`)
- Merge paired-end reads (`flash`)
- Split merged reads by amplicon (Python script)
- Look for chimeras (optional, `vsearch --vsearch_global`)
- Merge unique reads (Python script)
- Find species associated with each unique read (`vsearch`)
- Summarize results (Python script)
  - Tables of phylum, genus, and species counts per sample, including multiple hits
  - Number of reads remaining at each analysis step with figure
  - Most frequent non-annotated sequences to blast on NCBI nt/nr
  - Species counts for these non-annotated sequences

## Running the pipeline

For each new project, get a new copy of **Barque** from the sources listed in
the **Installation** section.

### Running on the test dataset

If you want to test **Barque**, jump straight to the `Test dataset` section at
the end of this file. Read through the README after to understand the program
and it's outputs.

### Preparing samples

Copy your paired-end sample files in the `04_data` folder. You need one pair of
files per sample. The sequences in these files must contain the sequences of
the primer that you used during the PCR.

The file names must follow this format:

```
SampleID_*_R1_001.fastq.gz
SampleID_*_R2_001.fastq.gz
```

Note that the sample name, or SampleID, must contain no underscore (`_`) and be
followed by an underscore (`_`). The star (`*`) can be any string of text that
**does not contain space characters**.

**If you do not have a dataset**, you can use the test dataset. See the **Test
dataset** section near the end of this file. In this case, you do not need to
modify the primer and config files.

### Formatting database

You will need to put a database in Fasta format in the `03_databases` folder.

An augmented version of the mitofish 12S database is already available in your
downloaded version of **Barque**

The pre-formatted BOLD database can be
[downloaded here](http://www.bio.ulaval.ca/louisbernatchez/files/bold.fasta.gz).

If you do not already have the indexed database and want to use BOLD, you will
need to download all the animal BINs from [this BOLD
page](http://www.boldsystems.org/index.php/Public_BarcodeIndexNumber_Home).
Put the downloaded Fasta files in `03_databases/bold_bins` (you will need to
create that folder), and run the commands to format the bold database:

- For other databases, get the database and format it:
  - Fasta format
  - Name line has 3 informations separated by an underscore (`_`)
  - Ex: `>Phylum_Genus_species`
  - Ex: `>Mammal_rattus_norvegicus`

```bash
# Format each BIN individually (~10 minutes)
# Note: the `species_to_remove.txt` file is optional
ls -1 03_databases/bold_bins/*.fas.gz |
    parallel ./01_scripts/util/format_bold_database.py \
    {} {.}_prepared.fasta.gz species_to_remove.txt

# Concatenate the resulting formatted bins into one file (~10 seconds)
gunzip -c 03_databases/bold_bins/*_prepared.fasta.gz > 03_databases/bold.fasta
```

### Configuration file

Make a copy of the file named `02_info/barque_config.sh` and modify the
parameters as needed.

### Launching Barque

Launch the `barque` executable with the name of your configuration file as an
argument, like this:

```bash
./barque 02_info/MY_CONFIG_FILE.sh
```

## Results

Once the pipeline has finished running, all result files are found in the
`12_results` folder.

After a run, it is recomended to make a copy of this folder and name it with the
current date, ex: `12_results_PROJECT_NAME_2019-10-08`

### Taxa count tables, named after the primer names

- `PRIMER_phylum_table.csv`
- `PRIMER_genus_table.csv`
- `PRIMER_species_table.csv`

### Sequence dropout report and figure

- `sequence_dropout.csv`: Listing how many sequences were present in each
sample for every analysis step. Depending on library and sequencing quality, as
well as the biological diversity found at the sample site, more or less
sequences are lost at each of the analysis steps. A figure is generated in
`sequence_dropout_figure.png`.

### Most frequent non-annotated sequences

- `most_frequent_non_annotated_sequences.fasta`: Sequences that are frequent in
the samples but were not annotated by the pipeline. This Fasta file should be
used to query the NCBI nt/nr database (**you will need to change the default
value**) using the online portal [found
here](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastSearch) to see
what species may have been missed. Use `blastn` with default parameters. Once
the NCBI blastn search is finished, download the results as a text file and use
the following command (you will need to adjust the input and output file names)
to generate a report of the most frequently found species in the non-annotated
sequences:

### Summarize species found in non-annotated sequences

```bash
./01_scripts/10_report_species_for_non_annotated_sequences.py \
    12_results/NCBI-Alignment.txt \
    12_results/most_frequent_non_annotated_sequences_species_ncbi.csv
```

The result file will contain one line per identified taxon and the number of
sequences for each taxon, sorted in decreasing order. For any species of
interest found in this file, it is a good idea to download the representative
sequences from NCBI, add them to the database, and rerun the analysis.

## Lather, Rinse, Repeat

Once the pipeline has been run, it is normal to find that unexpected species
have been found or that a proportion of the reads have not been identified,
either because the sequenced species are absent from the database or because
the sequences have the exact same distance from two or more sequences in the
database. In these cases, you will need to create a list of unwanted species to
be later removed from the database or download additional sequences for the
non-annotated species from NCBI to add them to the database. Once the database
has been improved, simply run the last part of the pipeline while using this
new database by making sure you have `SKIP_DATA_PREP=1` in your config file.
You may need to repeat this step again until you are satisfied with the
completeness of the results.

NOTE: You should provide justifications in your publications if you decide to
remove some species from the database.

## Test dataset

A test dataset is available as a [sister repository on
GitHub](https://github.com/enormandeau/barque_test_dataset). It is composed of
10 samples, each with 10,000 sequences (times two since it is a paired-end
dataset).

Download the repository and then move the data from
`barque_test_dataset/04_data` to **Barque**'s `04_data` folder.

If you have git and **Barque**'s dependencies installed, the following commands
will download the **Barque** repository and the test data and put them in the
appropriate folder.

```bash
git clone https://github.com/enormandeau/barque
git clone https://github.com/enormandeau/barque_test_dataset
cp barque_test_dataset/04_data/* barque/04_data/
cd barque
```

To run the analysis, move to the `barque` folder and launch:

```bash
./barque 02_info/barque_config.sh
```

The analysis of this test dataset takes 25 seconds on a Linux ThinkPad laptop
with 4 core-i7 CPUs from ~2012 and 70 seconds on the same laptop using only one
CPU.

## License

CC share-alike

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Barque</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Eric Normandeau</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/enormandeau/barque" rel="dct:source">https://github.com/enormandeau/barque</a>.
