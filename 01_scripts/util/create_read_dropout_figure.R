rm(list=ls())

data = read.table("12_results/sequence_dropout.csv", header=T, sep=",")
d = data[,2:ncol(data)]

percent_annotated = signif(100 * sum(d[,6]) / sum(d[,1]), 3)
png("12_results/sequence_dropout_figure.png", width=800, height=600)

plot(0, 0,
     type='n',
     xaxt='n',
     xlim=c(1, 6),
     ylim=c(min(as.matrix(d)), max(as.matrix(d))),
     main="Read dropout by analysis step in Barque",
     ylab="Number of reads",
     xlab="Analysis step")

axis(1, at=(1:6), labels=names(data)[2:ncol(data)])

for (i in 1:nrow(d)) {
    lines(1:6,
          d[i, ],
          col=i)
}

text(1,
     min(as.matrix(d)),
     cex=1.5,
     paste0("Annotated ",percent_annotated, "% of the reads globally"), adj=c(0, 0))

dev.off()
