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
wanted_species = "Gobiidae_Neogobius_melanostomus"

# Sort and print
dd = d[d$Sample %in% wanted_samples & d$Species == wanted_species, ]
dd.sorted = dd[order(dd$Similarity, decreasing=T),]
print(dd.sorted[order(dd.sorted$Sample),])

# Plot similarity by site for wanted species
par(mar=c(10, 4, 2, 2))
plot(dd$Similarity ~ as.factor(dd$Sample),
        las=2,
        main=paste("Similarity of hit for",wanted_species, "by sample"),
        xlab="",
        ylab="Hit similarity",
     ylim=c(min(d$Similarity)-0.2, 100.2)
     )

points(dd$Similarity ~ as.factor(dd$Sample),
       pch=19,
       col="#AA0011AA",
       cex=0.2*sqrt(dd$NumSequences+10))
