# Clear the workspace
rm(list = ls())

# Load required libraries
library(gridExtra)
library(ggplot2)
library(nortest)  # For Anderson-Darling test
library(psych)     # For skewness and kurtosis functions
library(ufs)

# Source or define the normalityAssessment function and its dependencies
# (Assuming the function is already available in your environment)

# Read the CSV file
data <- read.csv("Extraversion.csv", header = TRUE)

# Alternative approach: Analyze all scores together (pooled across participants)
all_scores <- unlist(data[, -1])
cat("\n\n=== Normality Assessment for ALL Participants Combined ===\n")
result_all <- normalityAssessment(all_scores, samples = 10000, digits = 3)

# Explicitly print results and plots
print(result_all)  # Isso mostrará estatísticas + plots no console

# Se quiser salvar também em arquivo (opcional)
sink("Extraversion_NormalityResults.txt")
print(result_all)
sink()