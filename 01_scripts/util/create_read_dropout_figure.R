rm(list=ls())

data = read.table("12_results/sequence_dropout.csv", header=T, sep=",")
names(data) = substring(names(data), 5)
d = data[,2:ncol(data)]
d[is.na(d)] = 0

numcol = ncol(d)
print(numcol)
if (numcol == 6) {
    figure_width = 800
} else {
    figure_width = 1800
}

print(head(data))
print(numcol)

percent_annotated = signif(100 * sum(d[, numcol]) / sum(d[,1]), 3)
trimmed_annotated = signif(100 * sum(d[, numcol]) / sum(d[,2]), 3)
chimera_annotated = signif(100 * sum(d[, numcol]) / sum(d[,5]), 3)
png("12_results/sequence_dropout_figure.png", width=figure_width, height=800)

plot(0, 0,
     type='n',
     xaxt='n',
     xlim=c(1,  numcol),
     ylim=c(0, max(as.matrix(d))),
     main="Read dropout by analysis step in Barque",
     ylab="Number of reads",
     xlab="Analysis step")

axis(1, at=(1: numcol), labels=names(data)[2:ncol(data)])

for (i in 1:nrow(d)) {
    lines(1: numcol,
          d[i, ],
          col=i)
}

text(1,
     0,
     cex=1.2,
     paste0("Annotated ", percent_annotated, "% of all reads (", trimmed_annotated, "% of trimmed reads, ", chimera_annotated, "% after chimera removal)"), adj=c(0, 0))

dev.off()
