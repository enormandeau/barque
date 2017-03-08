# Barque

## Version 1.2

### An environmental DNA metabarcoding analysis pipeline

![Barque](https://raw.githubusercontent.com/enormandeau/barque/master/00_archive/barque_small.png)

Developed by [Eric Normandeau](https://github.com/enormandeau) in
[Louis Bernatchez](http://www.bio.ulaval.ca/louisbernatchez/presentation.htm)'s
laboratory.

Please see licence information at the end of this file.

## Description

**Barque** is a metabarcoding dataset analysis pipeline that relies on high
quality metabarcoding databases instead of the generation of operational
taxonomic unit (OTUs). It is parallelized, fast, and streamlined.

## Installation

To use **Barque**, you will need a local copy of its repository, [found here](https://github.com/enormandeau/barque).

## Dependencies

You will also need to have the following programs installed on your computer.

- python 2.7
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
- Look for chimeras (`usearch -uchime_denovo`)
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
