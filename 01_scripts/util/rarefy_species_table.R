#!/usr/bin/env Rscript
# Cleanup
rm(list=ls())

# test if there is at least one argument: if not, return an error
args = commandArgs(trailingOnly=TRUE)
if (length(args)<3) {
    cat("Rarefy counts from the UNMODIFIED species count output of Barque\n\nUsage:\n    <program> input_counts num_reads num_iter\n\n")
    stop("Not enough parameters", call.=FALSE)

} else if (length(args)>=3) {
    # default output file
    input_file = args[1]
    num_reads = args[2]
    num_iterations = args[3]
}

# Modules
library(vegan)

# Loading data
count_table = read.table(input_file, header=T, sep=",")

# Subset the counts
counts = count_table[1:(nrow(count_table)-1), 6:ncol(count_table)]

# Iterations
for (iter in 1:num_iterations) {
    output_file = paste0(input_file, "_rarefied_", num_reads, "_iter_", iter, ".csv")
    rarefied = counts

    # Rarefy
    for (i in 1:ncol(counts)) {
        c = counts[, i]
        c = as.vector(rrarefy(c, num_reads))
        rarefied[, i] = c
    }

    # Construct output table and re-compute row and column tables
    rarefied_table = count_table
    rarefied_table[1:(nrow(count_table)-1), 6:ncol(count_table)] = rarefied
    rarefied_table[1:(nrow(count_table)-1), 5] = apply(rarefied, 1, sum)
    rarefied_table[nrow(count_table), 5:ncol(count_table)] = apply(rarefied_table[1:(nrow(count_table)-1), 5:ncol(count_table)], 2, sum)

    write.table(rarefied_table, output_file, col.names=T, row.names=F, quote=F, sep=",")
}
