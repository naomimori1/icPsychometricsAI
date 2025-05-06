# =============================================
# COMPLETE BFI-2 ANALYSIS WITH NORMALITY TESTS
# =============================================

# 1. Initial Setup -------------------------------------------------------
rm(list = ls())

# Safe package loading function
load_packages <- function() {
  suppressPackageStartupMessages({
    if (!require(psych)) install.packages("psych")
    if (!require(ggplot2)) install.packages("ggplot2")
    if (!require(dplyr)) install.packages("dplyr")
    if (!require(GPArotation)) install.packages("GPArotation")
    if (!require(tidyr)) install.packages("tidyr")
    if (!require(scales)) install.packages("scales")
    if (!require(gridExtra)) install.packages("gridExtra")
    if (!require(ggcorrplot)) install.packages("ggcorrplot")
    if (!require(ufs)) install.packages("ufs")
    
    library(psych)
    library(ggplot2)
    library(dplyr)
    library(GPArotation)
    library(tidyr)
    library(scales)
    library(gridExtra)
    library(ggcorrplot)
    library(ufs)
  })
}

load_packages()

# 2. Helper Functions ----------------------------------------------------
calculate_skewness <- function(x) {
  x <- x[!is.na(x)]
  n <- length(x)
  (sum((x - mean(x))^3)/n)/(sum((x - mean(x))^2)/n)^(3/2)
}

# 3. Data Loading and Preparation ----------------------------------------
# Load response data
data <- read.csv("Psycho50.csv", header = TRUE, row.names = 1)

# Check data structure
str(data)

# Check for missing values
sum(is.na(data))

# BFI-2 structure
bfi2_structure <- list(
  Extraversion = c(1, 6, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56),
  Agreeableness = c(2, 7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 57),
  Conscientiousness = c(3, 8, 13, 18, 23, 28, 33, 38, 43, 48, 53, 58),
  Negative_Emotionality = c(4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59),
  Open_Mindedness = c(5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60)
)

# Item reversal
reverse_items <- function(data) {
  items_to_reverse <- c(3,4,5,8,9,11,12,16,17,22,23,24,25,26,28,29,30,
                       36,37,42,44,45,47,48,49,50,51,55,58,59)
  data[, items_to_reverse] <- 6 - data[, items_to_reverse]
  return(data)
}

reversed_data <- reverse_items(data)

# 4. Domain Score Calculation --------------------------------------------
calculate_domain_scores <- function(data, structure) {
  domain_scores <- data.frame(row.names = rownames(data))
  
  for (domain in names(structure)) {
    items <- structure[[domain]]
    domain_scores[[domain]] <- rowMeans(data[, items], na.rm = TRUE)
  }
  
  return(domain_scores)
}

domain_scores <- calculate_domain_scores(reversed_data, bfi2_structure)

# 5. Normality Assessment -----------------------------------------------
normality_results <- list()

for (domain in colnames(domain_scores)) {
  cat("\n=== NORMALITY ASSESSMENT FOR:", domain, "===\n")
  
  normality_results[[domain]] <- normalityAssessment(
    domain_scores[[domain]],
    samples = 1000,
    digits = 3,
    xLabel.sampleDist = paste(domain, "Scores"),
    xLabel.samplingDist = paste("Sampling Distribution of", domain, "Means")
  )
  
  print(normality_results[[domain]])
}

# 6. Descriptive Statistics ---------------------------------------------
item_stats <- describe(reversed_data) %>%
  as.data.frame() %>%
  tibble::rownames_to_column("Item") %>%
  mutate(Item = as.numeric(gsub("X", "", Item)),
         Domain = sapply(Item, function(x) {
           names(bfi2_structure)[sapply(bfi2_structure, function(y) x %in% y)]
         })) %>%
  select(Item, Domain, n, mean, sd, median, min, max, skew, kurtosis) %>%
  mutate(across(where(is.numeric), round, 3))

domain_stats <- data.frame()
for (domain in names(bfi2_structure)) {
  scores <- domain_scores[[domain]]
  domain_stats <- rbind(domain_stats,
                       data.frame(Domain = domain,
                                 Mean = round(mean(scores), 3),
                                 SD = round(sd(scores), 3),
                                 Median = round(median(scores), 3),
                                 Min = round(min(scores), 3),
                                 Max = round(max(scores), 3),
                                 Skewness = round(calculate_skewness(scores), 3),
                                 Kurtosis = round(kurtosi(scores), 3)))
}

# 7. Visualization ------------------------------------------------------
# Histograms of domain scores
plot_domain_distributions <- function() {
  plots <- list()
  for (domain in colnames(domain_scores)) {
    df <- data.frame(Score = domain_scores[[domain]])
    
    plots[[domain]] <- ggplot(df, aes(x = Score)) +
      geom_histogram(aes(y = ..density..), bins = 15, 
                     fill = "skyblue", color = "black") +
      geom_density(color = "red", size = 1) +
      ggtitle(paste(domain, "Distribution")) +
      theme_minimal()
  }
  grid.arrange(grobs = plots, ncol = 2)
}

plot_domain_distributions()

# Correlation matrix between domains
plot_domain_correlations <- function() {
  cor_matrix <- cor(domain_scores)
  ggcorrplot(cor_matrix, 
             hc.order = TRUE,
             type = "lower",
             lab = TRUE,
             title = "Domain Score Correlations")
}

plot_domain_correlations()

# 8. Save Results -------------------------------------------------------
write.csv(item_stats, "bfi2_item_statistics.csv", row.names = FALSE)
write.csv(domain_stats, "bfi2_domain_statistics.csv", row.names = FALSE)

# Save normality test results
normality_summary <- data.frame(
  Domain = names(normality_results),
  ShapiroWilk_p = sapply(normality_results, function(x) x$sw.sampleDist$p.value),
  AndersonDarling_p = sapply(normality_results, function(x) x$ad.sampleDist$p.value),
  Skewness = sapply(normality_results, function(x) x$dataShape.sampleDist$skewness),
  Kurtosis = sapply(normality_results, function(x) x$dataShape.sampleDist$kurtosis),
  stringsAsFactors = FALSE
)

write.csv(normality_summary, "bfi2_normality_results.csv", row.names = FALSE)