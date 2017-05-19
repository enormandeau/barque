#!/bin/bash

# Modify the following parameter values according to your experiment
# Do not modify the parameter names or remove some parameters
# Do not add spaces around the equal (=) sign

# Global parameters
NCPUS=10                    # Number of CPUs to use for analyses (int, 1+)

# Skip data preparation and rerun only from vsearch
SKIP_DATA_PREP=0            # 1 to skip data preparation steps, 0 to run full pipeline

# Merging reads with flash
MIN_OVERLAP=30              # Minimum number of overlapping nucleotides to merge reads (int, 1+)
MAX_OVERLAP=280             # Maximum number of overlapping nucleotides to merge reads (int, 1+)

# Running or skipping chimera detection
LOOK_FOR_CHIMERA=1          # 1 to search for chimeras (RECOMMENDED), 0 to skip chimera detection
                            #   or use already created chimera cleaned files

# vsearch
SIMILARITY_VSEARCH=0.97     # Minimum similarity to database to keep in intermediate results (float, 0-1)
MAX_ACCEPTS=10              # Accept at most this number of sequences before stoping search (int, 1+)
MAX_REJECTS=50              # Reject at most this number of sequences before stoping search (int, 1+)
QUERY_COV=0.6               # At least that proportion of the sequence must match the database (float, 0-1)

# Filters
MIN_HIT_LENGTH=100          # Minimum vsearch hit length to keep in results (int, 1+)
MIN_HITS_SAMPLE=1           # Minimum number of hits a species must have in at least one sample
                            #   to keep in results (int, 1+)
# Non-annotated reads
NUM_NON_ANNOTATED_SEQ=1000  # Number of unique most-frequent non-annotated reads to keep (int, 1+)
