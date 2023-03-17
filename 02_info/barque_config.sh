#!/bin/bash

# Modify the following parameter values according to your experiment
# Do not modify the parameter names or remove parameters
# Do not add spaces around the equal (=) sign
# It is a good idea to try to run Barque with different parameters 

# Global parameters
NCPUS=40                    # Number of CPUs to use. A lot of the steps are parallelized (int, 1+)
PRIMER_FILE="02_info/primers.csv" # File with PCR primers information

# Skip data preparation and rerun only from vsearchp
SKIP_DATA_PREP=0            # 1 to skip data preparation steps, 0 to run full pipeline (recommended)

# Filtering with Trimmomatic
CROP_LENGTH=200             # Cut reads to this length after filtering. Just under amplicon length

# Merging reads with flash
MIN_OVERLAP=30              # Minimum number of overlapping nucleotides to merge reads (int, 1+)
MAX_OVERLAP=280             # Maximum number of overlapping nucleotides to merge reads (int, 1+)

# Extracting barcodes
MAX_PRIMER_DIFF=8           # Maximum number of differences allowed between primer and sequence (int, 0+)

# Running or skipping chimera detection
SKIP_CHIMERA_DETECTION=0    # 0 to search for chimeras (RECOMMENDED), 1 to skip chimera detection
                            #   or use already created chimera cleaned files

# vsearch
MAX_ACCEPTS=20              # Accept at most this number of sequences before stoping search (int, 1+)
MAX_REJECTS=20              # Reject at most this number of sequences before stoping search (int, 1+)
QUERY_COV=0.6               # At least that proportion of the sequence must match the database (float, 0-1)
MIN_HIT_LENGTH=100          # Minimum vsearch hit length to keep in results (int, 1+)

# Filters
MIN_HITS_SAMPLE=1           # Minimum number of hits in at least one sample  to keep in results (int, 1+)
MIN_HITS_EXPERIMENT=1       # Minimum number of hits in whole experiment to keep in results (int, 1+)

# Non-annotated reads
NUM_NON_ANNOTATED_SEQ=200   # Number of unique most-frequent non-annotated reads to keep (int, 1+)

# OTUs
SKIP_OTUS=1                 # 1 to skip OTU creation, 0 to use it
MIN_SIZE_FOR_OTU=1          # Only unique reads with at least this coverage will be used for OTUs
