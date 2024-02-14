# Cleanup and load data
rm(list=ls())
d = read.table("similarity_by_species_and_site.tsv", header=T)

# Print species and sample names
samples = sort(unique(d$Sample))
species = sort(unique(d$Species))
print(samples)
print(species)

# Select wanted samples and species
wanted_samples = samples #c("sample-01", "sample-05")
wanted_species = "Agonidae_Ulcina_olrikii"

# Sort and print
dd = d[d$Sample %in% wanted_samples & d$Species == wanted_species, ]
dd.sorted = dd[order(dd$Similarity, decreasing=T),]
print(dd.sorted[order(dd.sorted$Sample),])

# Plot similarity by site for wanted species
par(mar=c(10, 4, 3, 2))
plot(dd$Similarity ~ as.factor(dd$Sample),
        las=2,
        main=paste("Similarity of hit by sample for:  ",wanted_species, "\n(circle surface proportional to number of reads)"),
        xlab="",
        ylab="Hit similarity",
     ylim=c(min(d$Similarity)-0.2, 100.2)
     )

points(dd$Similarity ~ as.factor(dd$Sample),
       pch=19,
       col="#AA0011AA",
       cex=0.1*sqrt(dd$NumSequences+5))
