#!/usr/bin/env python3
"""Replace species counts below a proportion (eg: 0.001) by zero

Usage:
    <program> input_csv proportion output_csv
"""

# Modules
import pandas as pd
import sys

# Parsing user input
try:
    input_csv = sys.argv[1]
    proportion = float(sys.argv[2])
    output_csv = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Read csv
df = pd.read_csv(input_csv)

for col in list(df.columns)[5:]:
    # Compute threshold
    total = sum(df[col])
    threshold = int(float(total) * proportion)

    # Replace counts lower than threshold by zero
    df.loc[df[col] < threshold, col] = 0

    # Get new total
    total = sum(df[col])
    df.at[df.index[-1], col] = total

# Recompute total per row
for row in df.index:

    total = sum(df.iloc[row, 5:])
    df.loc[row, "Total"] = total

# Write output file
df.to_csv(output_csv, index=False)
