# eDNA pipeline

This eDNA pipeline was developed by Eric Normandeau in Louis Bernatchez's
laboratory. See licence information at the end of this file.

## Analysis overview
- Format databases (Python scripts)
- Filter and trim (trimmomatic, length)
- Merge paired-end (flash)
- Split by amplicon (Python script)
- Merge all samples per amplicon (bash script)
- Find chimeras (usearch `-uchime_denovo`)
    - None detectable above 270 bp
- (Maybe) Merge unique reads (save 50-80% of usearch time)
- Find species (usearch)
    - (done) Find duplicate species (use 40 best hits)
    - (done) Give list of multiple hits to Anaïs
    - (done) Add unwanted species to `species_to_remove.txt`
    - (done) Reformat bold database + `makeudb_usearch`
    - (done) Redo a run to find multiple hits until there is no more (lower 40 -> 20 for speed)
- Format results for interpretation and publication
- **Summarize analyses**
    - Number of reads at each step
    - Quality of Fastq files at each step

## Improve folders
- `02_info_files` (contains iupac.csv, primers.csv, illumina_adapters.fas)
- `03_databases`
- `04_data`
- ...

## Create helpful README.md
- Dependencies
- How to use

## Add makefile to automate analyses

## License
CC share-alike, commercial permitted

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">eDNA pipeline</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Eric Normandeau</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/enormandeau/edna_pipeline" rel="dct:source">https://github.com/enormandeau/edna_pipeline</a>.
