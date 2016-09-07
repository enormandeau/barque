# Bernatchez lab eDNA pipeline

## Analysis overview
- Format databases (Python scripts)
  - Silva phyla seem strange. Keep only those in a certain list?
  - Number of silva sequences is very low and only 1 seq/species
x Filter and trim (trimmomatic, length)
x Merge paired-end (flash)
x Split by amplicon (Python script)
x Merge all samples per amplicon (bash script)
.. Find chimeras (usearch `-uchime_denovo`)
- Remove chimeras
  - Merged samples
  - Separate samples
- Find species (usearch)
  - Split samples
  - Merged samples (do only split and regroup results?)
  - Both COI and 18S
- Format results for interpretation and publication
  - split / merged
  - COI / 18S
  - Genus / phylum

## Improve folders
- `02_info_files`
- `03_databases`
- `04_data`
- ...

## Create helpful README.md
- Author=me, developped in Bernatchez lab
- Dependencies
- How to use

## Add makefile to automate analyses

## License
CC share-alike, commercial permitted

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">eDNA pipeline</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Eric Normandeau</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/enormandeau/edna_pipeline" rel="dct:source">https://github.com/enormandeau/edna_pipeline</a>.
