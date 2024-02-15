#!/usr/bin/env Rscript
# Cleanup and load data
rm(list=ls())
d = read.table("12_results/similarity_by_species_and_site.tsv", header=T)

# Print species and sample names
samples = sort(unique(d$Sample))
species = sort(unique(d$Species))

# Select wanted samples and species
wanted_samples = samples #c("sample-01", "sample-05")

# TODO Produce jpeg 1 image per species in subfolder
for (wanted_species in species) {

    dd = d[d$Sample %in% wanted_samples & d$Species == wanted_species, ]

    # Plot similarity by site for wanted species
    png(paste0("12_results/figures_similarity_by_species/similarity_",
               wanted_species, ".png"),
        width=1000, height=400)

        par(mar=c(10, 4, 3, 2))
        max_reads = max(dd$NumSequences)

        # Barplot
        plot(dd$Similarity ~ as.factor(dd$Sample),
             las=2,
             main=paste("Similarity of hit by sample for:  ",
                        wanted_species,
                        "\n( circle sizes proportional to number of reads, max reads:",
                        max_reads, ")"),
             xlab="",
             ylab="Hit similarity",
             ylim=c(min(d$Similarity)-0.2, 100.2)
        )

        # DEBUG
        abline(h=98, col="red", lty=2)
        abline(h=97, col="black", lty=2)

        # Add points with sizes correlated to number of sequences
        points(dd$Similarity ~ as.factor(dd$Sample),
               pch=19,
               col="#AA001199",
               cex=sqrt(20 * dd$NumSequences / max_reads))

    dev.off()
}
