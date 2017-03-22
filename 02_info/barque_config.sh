#!/bin/bash

# Modify the following parameter values according to your experiment
# Do not modify the parameter names or remove some parameters

# Global parameters
NCPUS=16                # Number of CPUs to use for analyses (int, 1+)

# Skip data preparation and rerun only from usearch
SKIP_DATA_PREP=0        # 1 to skip data preparation steps, 0 to run full pipeline

# Merging reads with flash
MIN_OVERLAP=30          # Minimum number of overlapping nucleotides to merge reads (int, 1+)
MAX_OVERLAP=280         # Maximum number of overlapping nucleotides to merge reads (int, 1+)

# Running or skipping chimera detection
LOOK_FOR_CHIMERA=1      # 1 to search for chimeras, 0 to skip (can be LONG for big samples)

# Usearch
SIMILARITY_USEARCH=0.95 # Minimum similarity to database to keep in intermediate results (float, 0-1)
MAX_ACCEPTS=10          # Accept at most this number of sequences before stoping search (int, 1+)
MAX_REJECTS=50          # Reject at most this number of sequences before stoping search (int, 1+)
QUERY_COV=0.6           # At least that proportion of the sequence must match the database (float, 0-1)

# Filters
SIMILARITY_RESULTS=0.96 # Minimum similarity to database to keep in results (float, 0-1)
MIN_HIT_LENGTH=100      # Minimum usearch hit length to keep in results (int, 1+)
MIN_HITS_SAMPLE=1       # Minimum number of hits a species must have in at least one sample
                        #   to keep in results (int, 1+)
