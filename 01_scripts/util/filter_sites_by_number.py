#!/usr/bin/env python3
"""Replace species counts below a threshold (eg: 10) by zero

Usage:
    <program> input_csv threshold min_count output_csv
"""

# Modules
import pandas as pd
import sys

# Parsing user input
try:
    input_csv = sys.argv[1]
    threshold = int(sys.argv[2])
    min_count = int(sys.argv[3])
    output_csv = sys.argv[4]
except:
    print(__doc__)
    sys.exit(1)

# Read csv
df = pd.read_csv(input_csv)

for col in list(df.columns)[5:]:
    # Compute threshold
    total = sum(df[col])
    # placeholder comment line

    # Replace counts lower than threshold by zero
    df.loc[df[col] < threshold, col] = 0

# Recompute totals per column
for col in df.columns[5: ]:
    total = sum(df[col][: -1])

    #df[col].loc[-1] = total
    df.iloc[-1, df.columns.get_loc(col)] = total

# Recompute total per row
for row in df.index:
    total = sum(df.iloc[row, 5:])
    df.loc[row, "Total"] = total

# Remove species with zero count
df = df[df["Total"] >= min_count]

# Write output file
df.to_csv(output_csv, index=False)
