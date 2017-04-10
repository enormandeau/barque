# Before 1.3

## Benchmarking
- Victoria's dataset first 100k sequences per sample
  - Find way to get time plus CPU and memory usage through time

## Documentation
- Describe input sequence format requirements
  - file name
  - fastq and/or fastq.gz
- Describe test dataset on `github.com/enormandeau/barque_test_dataset`
  - Include good `primers.csv` file

## Finish paper
- Finish first draft
- Add references

-----------------------------------------------------------------------------

# Later

## Features
- R scripts to produce read dropout and count table figures
- Report barcode splitting results for each sample
- Support single-end data (no merge -> pseudo-merge script)
- Support interleaved input (flash can treat it)

## Performance
- Run `vsearch --usearch_global` in parallel
- Have 2 values for the number of CPUs:
  - For data preparation steps (read-write intensive)
  - For the vsearch steps (computation intensive)
- Blast only unique sequences for the whole dataset (v2.0)
  (big boost if lots of samples)
  - Create dictionary of unique reads
  - Blast them and store results
  - Assign results to each read of each pop
- Parallelize read dropout computation
  - Make functions and call them with parallel
  - or launch in background and `wait` to summarize
