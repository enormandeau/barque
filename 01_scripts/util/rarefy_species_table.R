# Cleanup
rm(list=ls())

# Modules
library(vegan)

# Global variables
num_reads = 1000
num_iterations = 100
input_file = "12s200pb_species_table.csv"

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
  
  write.table(rarefied_table, output_file, col.names=T, row.names=F, sep=",")
}