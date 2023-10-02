# Barque v1.8.0

## Environmental DNA metabarcoding analysis

![Barque](https://raw.githubusercontent.com/enormandeau/barque/master/00_archive/barque_small.png)

Developed by [Eric Normandeau](https://github.com/enormandeau) in
[Louis Bernatchez](http://www.bio.ulaval.ca/louisbernatchez/presentation.htm)'s
laboratory.

Licence information at the end of this file.

## Description

**Barque** is a fast eDNA metabarcoding analysis pipeline that annotates
denoised ASVs (or Optionally OTUs), using high-quality barcoding databases.

**Barque** can produce OTUs, which are then annotated using a database. These
annotated OTUs are then used as a database themselves to find read counts per
OTU per sample, effectively "annotating" the reads with the OTUs that were
previously found.

## Citation
Barque is described as an accurate and efficient eDNA analysis pipeline in:

**Mathon L, Guérin P-E, Normandeau E, Valentini A, Noel C, Lionnet C, Linard B,
Thuiller W, Bernatchez L, Mouillot D, Dejean T, Manel S. 2021. Benchmarking
bioinformatic tools for fast and accurate eDNA metabarcoding species
identification. Molecular Ecology Resources.**

https://onlinelibrary.wiley.com/doi/abs/10.1111/1755-0998.13430

## Use cases

- Monitoring invasive species
- Confirming the presence of specific species
- Characterizing meta-communities in varied environments
- Improving species distribution knowledge of cryptic taxa
- Following loss of species over medium to long-term monitoring

Since **Barque** depends on the use of high-quality barcoding databases, it is
especially useful for amplicons that already have large databases, like COI
amplicons from the Barcode of Life Database (BOLD) or 12S amplicons from the
mitofish database, although it can also use any database, for example the Silva
database for the 18s gene or any other custom database. If for some reason
species annotations are not possible, **Barque** can be used in OTU mode.

## Installation

To use **Barque**, you will need a local copy of its repository. Different
releases can be [found here](https://github.com/enormandeau/barque/releases).
It is recommended to always use the latest release or even the development
version. You can either download an archive of the latest release at the above
link or get the latest commit (recommended) with the following git command:

```
git clone https://github.com/enormandeau/barque
```

### Dependencies

To run **Barque**, you will also need to have the following programs installed
on your computer.

- **Barque** will only work on GNU Linux or OSX
- bash 4+
- python 3.5+ (you can use miniconda3 to install python)
- R 3+ (ubuntu/mint: `sudo apt-get install r-base-core`)
- java (ubuntu/mint: `sudo apt-get install default-jre`)
- [gnu parallel](https://www.gnu.org/software/parallel/)
- [flash (read merger)](https://ccb.jhu.edu/software/FLASH/) v1.2.11+
- [vsearch](https://github.com/torognes/vsearch/releases) v2.14.2+
  - /!\ **v2.14.2+ required** /!\
  - **Barque will not work with older versions of vsearch**

### Preparation

- Install dependencies
- Download a copy of the **Barque** repository (see **Installation** above)
- Edit `02_info/primers.csv` to provide information describing your primers
- Get or prepare the database(s) (see Formatting database section below) and
  deposit the `fasta.gz` file in the `03_databases` folder and give it a name
  that matches the information of the `02_info/primers.csv` file.
- Modify the parameters in `02_info/barque_config.sh` for your run
- Launch **Barque**, for example with `./barque 02_info/barque_config.sh`

## Overview of Barque steps

During the analyses, the following steps are performed:

- Filter and trim raw reads (`trimmomatic`)
- Merge paired-end reads (`flash`)
- Split merged reads by amplicon (Python script)
- Look for chimeras and denoise reads (`vsearch --vsearch_global`)
- Merge unique reads (Python script)
- Find species associated with unique, denoised reads (`vsearch`)
- Summarize results (Python script)
  - Tables of phylum, genus, and species counts per sample, including multiple hits
  - Number of retained reads per sample at each analysis step with figure
  - Most frequent non-annotated sequences to blast on NCBI nt/nr
  - Species counts for these non-annotated sequences
  - Sequence groups for cases of multiple hits

## Running the pipeline

For each new project, get a new copy of **Barque** from the source listed in
the **Installation** section. In this case, you do not need to modify the
primer and config files.

### Running on the test dataset

If you want to test **Barque**, jump straight to the `Test dataset` section at
the end of this file. Later, be sure to read through the README to understand
the program and it's outputs.

### Preparing samples

Copy your paired-end sample files in the `04_data` folder. You need one pair of
files per sample. The sequences in these files must contain the sequences of
the primer that you used during the PCR. Depending on the format in which you
received your sequences from the sequencing facility, you may have to proceed
to demultiplexing before you can use **Barque**.

**IMPORTANT:** The file names must follow this format:

```
SampleID_*_R1_001.fastq.gz
SampleID_*_R2_001.fastq.gz
```

Notes: Each sample name, or SampleID, must contain no underscore (`_`) and be
followed by an underscore (`_`). The star (`*`) can be any string of text that
**does not contain space characters**. For example, you can use dashes (`-`) to
separate parts of your sample names, eg: `PopA-sample001_ANYTHING_R1_001.fastq.gz`.

### Formatting database

You need to put a database in gzip-compressed Fasta format, or `.fasta.gz`, in
the `03_databases` folder.

An augmented version of the mitofish 12S database is already available in
**Barque**.

The pre-formatted BOLD database can be
[downloaded here](http://www.bio.ulaval.ca/louisbernatchez/files/bold.fasta.gz).

If you want to use a newer version of the BOLD database, you will need to
download all the animal BINs from [this page
](http://www.boldsystems.org/index.php/Public_BarcodeIndexNumber_Home). Put
the downloaded Fasta files in `03_databases/bold_bins` (you will need to create
that folder), and run the commands to format the bold database:

```bash
# Format each BIN individually (~10 minutes)
# Note: the `species_to_remove.txt` file is optional
ls -1 03_databases/bold_bins/*.fas.gz |
    parallel ./01_scripts/util/format_bold_database.py \
    {} {.}_prepared.fasta.gz species_to_remove.txt

# Concatenate the resulting formatted bins into one file
gunzip -c 03_databases/bold_bins/*_prepared.fasta.gz > 03_databases/bold.fasta
```

- For other databases, get the database and format it:
  - gzip-compressed Fasta format (`.fasta.gz`)
  - Name lines must contain 3 information fields separated by an underscore (`_`)
  - Ex: `>Phylum_Genus_species`
  - Ex: `>Family_Genus_species`
  - Ex: `>Mammal_rattus_norvegicus`

### Configuration file

Modify the parameters in `02_info/barque_config.sh` as needed.

### Launching Barque

Launch the `barque` executable with the name of your configuration file as an
argument, like this:

```bash
./barque 02_info/barque_config.sh
```

## Reducing false positives

Two of the parameters in the config file can help reduce the presence of false
positive annotations in the results: `MIN_HITS_EXPERIMENT` and
`MIN_HITS_SAMPLE`. The defaults to both of these are very permissive and should
be modified if false positives are problematic in the results. Additionally,
the following script is provided to filter out species annotations that fall
below a minimum proportion of reads in each samples:
`filter_sites_by_proportion.py`. This filter is especially useful if the
different samples have very unequal numbers of reads. Having a high quality
database will also help reducing false annotations. Finally, manual curation of
the results if recommended with any eDNA analysis, whatever the software used.

## Results

Once the pipeline has finished running, all result files are found in the
`12_results` folder.

After a run, it is recommended to make a copy of this folder and name it with the
current date, ex:

```bash
cp -r 12_results 12_results_PROJECT_NAME_2020-07-27_SOME_ADDITIONAL_INFO
```

### Taxa count tables, named after the primer names

- `PRIMER_genus_table.csv`
- `PRIMER_phylum_table.csv`
- `PRIMER_species_table.csv`

### Sequence dropout report and figure

- `sequence_dropout.csv`: Listing how many sequences were present in each
sample for every analysis step. Depending on library and sequencing quality, as
well as the biological diversity found at the sample site, more or less
sequences are lost at each of the analysis steps. The figure
`sequence_dropout_figure.png` shows how many sequences are retained for each
sample at each step of the pipeline.

### Most frequent non-annotated sequences

- `most_frequent_non_annotated_sequences.fasta`: Sequences that are frequent in
the samples but were not annotated by the pipeline. This Fasta file should be
used to query the NCBI nt/nr database using the online portal [found
here](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastSearchhttps://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastSearch)
to see what species may have been missed. Use `blastn` with default parameters.
Once the NCBI blastn search is finished, download the results as a text file
and use the following command (you will need to adjust the input and output
file names) to generate a report of the most frequently found species in the
non-annotated sequences:

### Fasta files with sequences from multiple hit groups

- `12_results/01_multihits` contains fasta file with database and sample
  sequences to help understand why some of the sequences cannot be unambiguously
  assigned to one species. For example, sometimes two different species can have
  identical reads in the database. At other times, sample sequences can have the
  same distance to sequences of two different species in the database.

### Summarize species found in non-annotated sequences

```bash
./01_scripts/10_report_species_for_non_annotated_sequences.py \
    12_results/NCBI-Alignment.txt \
    12_results/most_frequent_non_annotated_sequences_species_ncbi.csv 97 |
    sort -u -k 2,3 | cut -c 2- | perl -pe 's/ /\t/' > missing_species_97_percent.txt
```

The first result file will contain one line per identified taxon and the number
of sequences for each taxon, sorted in decreasing order. For any species of
interest found in this file, it is a good idea to download the representative
sequences from NCBI, add them to the database, and rerun the analysis.

You can modify the percentage value, here 97. The
`missing_species_97_percent.txt` file will list the sequence identifiers from
NCBI so that you can download them from the online database and add them to
your own database as needed.

One way to do this automatically is to make a file with only the first column,
that is: one NCBI sequence identifier per line, and load it on this page:

https://www.ncbi.nlm.nih.gov/sites/batchentrez

You will need to rename the sequences to follow the database name format
described in the **Formatting database** section and add them to your current
database.

### Log files and parameters

For each **Barque** run, three files are written in the `99_logfiles` folder.
Each contain a timestamp with the time of the run:

1. The exact barque config file that has been used
1. The exact primer file as it was used
1. The full log of the run

## Lather, Rinse, Repeat

Once the pipeline has been run, it is normal to find that unexpected species
have been found or that a proportion of the reads have not been identified,
either because the sequenced species are absent from the database or because
the sequences have the exact same distance from two or more sequences in the
database. In these cases, you will need to remove unwanted species from the
database or download additional sequences for the non-annotated species from
NCBI to add them to it. Once the database has been improved, simply run the
pipeline again with this new database. You can put`SKIP_DATA_PREP=1`
in your config file if you wish to avoid repeating the initial data
preparation steps of **Barque**. You may need to repeat this procedure again
until you are satisfied with the completeness of the results.

NOTE: You should provide justifications in your publications if you decide to
remove some species from the results or database.

## Test dataset

A test dataset is available as a [sister repository on
GitHub](https://github.com/enormandeau/barque_test_dataset). It is composed of
10 mitofish-12S metabarcoding samples, each with 10,000 forward and 10,000
reverse sequences.

Download the repository and then move the data from
`barque_test_dataset/04_data` to **Barque**'s `04_data` folder.

If you have git and **Barque**'s dependencies installed, the following commands
will download the **Barque** repository and the test data and put them in the
appropriate folder.

```bash
git clone https://github.com/enormandeau/barque
git clone https://github.com/enormandeau/barque_test_dataset
cp barque_test_dataset/04_data/* barque/04_data/
```

To run the analysis, move to the `barque` folder and launch:

```bash
cd barque
./barque 02_info/barque_config.sh
```

The analysis of this test dataset takes 25 seconds on a Linux ThinkPad laptop
from 2012 running with 4 core-i7 CPUs and 70 seconds on the same laptop using
only one CPU.

## License

CC share-alike

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Barque</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Eric Normandeau</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
