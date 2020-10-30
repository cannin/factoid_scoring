library(ROCR)

reach_count <- read.csv("jwong_data/all_pmids_abstracts_scores_mod_types.csv")
suitable_now <- readLines("jwong_data/hit_pmids.txt")
all <- readLines("jwong_data/all_pmids.txt")

score_col <- c("score", "mod_score")
tmp <- data.frame(pmid=all, suitable_now=0, reach_count=0, stringsAsFactors=FALSE)
tmp[tmp$pmid %in% suitable_now, "suitable_now"] <- 1
tmp[, c("reach_count", "reach_count_mod")] <- reach_count[match(all, reach_count$pmid), score_col]
tmp <- tmp[complete.cases(tmp),]
tmp <- merge(tmp, reach_count[, c("pmid", "types")], by="pmid", all.x=TRUE)
write.csv(tmp, "all_pmids_reach_score.csv", row.names = FALSE, quote = FALSE)
#tmp[, "reach_count"] <- ifelse(tmp[, "reach_count"] >= 1, 1, 0)

# From: pubmed_search_pmid.R
# https://rviews.rstudio.com/2019/03/01/some-r-packages-for-roc-curves/
now <- tmp[, c("suitable_now", "reach_count", "reach_count_mod")]

# prediction(predictions, labels)
pred <- prediction(now$reach_count, now$suitable_now)
perf <- performance(pred, "tpr", "fpr")
plot(perf, main="Suitable Now")
abline(0, 1, lty = 2)
gain <- performance(pred, "tpr", "rpp")
plot(gain, main = "Gain Chart")
# https://heuristically.wordpress.com/2009/12/18/plot-roc-curve-lift-chart-random-forest/
lift <- performance(pred, "lift", "rpp")
plot(lift, main="Lift Chart")

# prediction(predictions, labels)
# AUC: Cutoffs: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2935260/
# * 0.9-1: Excellent
# * 0.8-0.9: Good
# * 0.7-0.8: Fair 
# * 0.6-0.7: Poor 
# * 0.5-0.6: Bad
pred <- prediction(now$reach_count, now$suitable_now)
perf <- performance(pred, "tpr", "fpr")
auc <- performance(pred, "auc") 
auc1 <- unlist(slot(auc, "y.values"))
auc1 

pred <- prediction(now$reach_count_mod, now$suitable_now)
perf2 <- performance(pred, "tpr", "fpr")
auc <- performance(pred, "auc") 
auc2 <- unlist(slot(auc, "y.values"))
auc2

plot(perf, col="red", main="Suitable Now")
plot(perf2, add = TRUE, col="blue")

# Gain Curve (Custom)
# Creating the data frame
score_col <- "reach_count"
df <- now[, c("suitable_now", score_col)]

# Ordering the dataset
df <- df[order(-df[, score_col]),]

# FIXME
df$baseline <- seq(from = 0,
                   to = length(which(df$suitable_now == 1)),
                   length.out = nrow(df))

# Creating the cumulative density
df$reach_count_model_prcnt <- cumsum(df$suitable_now)/sum(df$suitable_now)
df$cumulative_baseline <- cumsum(df$suitable_now)
df$cumulative_baseline_prcnt <- df$baseline/sum(df$suitable_now)
df$ratio_reach_baseline <- df$reach_count_model_prcnt / df$cumulative_baseline_prcnt

# Creating the % of population
df$sample_percent <- (seq(nrow(df))/nrow(df))*100

# Plotting
plot(df$sample_percent, 
     df$reach_count_model_prcnt, 
     type="l", 
     xlab="% of Available Papers", 
     ylab="% of Suitable Now Papers",
     main="% of Suitable Now Papers Found at\nVarious REACH Interaction Counts (in Red)")
lines(df$sample_percent, df$cumulative_baseline_prcnt)

cnts <- unique(df[, score_col])
pts <- sapply(cnts, function(i) {
  #i <- 7
  idx <- which(df[, score_col] == i)
  idx[length(idx)]  
})
names(pts) <- cnts

for(i in 1:length(pts)) {
  #i <- 5
  pt <- pts[i]
  name <- names(pts)[i]
  cat("PT: ", pt, " NAME: ", name, "\n")
  x <- df$sample_percent[pt]
  y <- df$reach_count_model_prcnt[pt]
  w <- x*nrow(reach_count)/100
  z <- y*length(suitable_now)
  cat("X: ", x, " Y: ", y, " W: ", w, " Z: ", z, " W-Z: ", w-z, " (W-Z)/W: ", round((w-z)/w,2), "\n")
  text(x, y, labels=name, col="red", cex=0.75)
}

abline(v=df$sample_percent[pts["1"]], col="red")
abline(h=df$reach_count_model_prcnt[pts["1"]], col="red")

df <- round(df, 2)