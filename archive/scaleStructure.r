# Load required libraries
library(psych)
library(ufs)

# Read the data
data <- read.csv("Extraversion.csv", header = TRUE)

# Extract just the item scores (excluding the first column with participant IDs)
item_scores <- data[, -1]

# Run the scale reliability analysis
results <- scaleStructure(
  dat = item_scores,
  digits = 3,          # Number of decimal places to display
  ci = TRUE,           # Compute confidence intervals
  interval.type = "normal-theory",  # CI calculation method
  conf.level = 0.95,   # 95% confidence intervals
  omega.psych = TRUE,  # Include omega from psych package
  poly = TRUE          # Compute ordinal reliability estimates
)

# Print the results
print(results)

# Save results to a text file
sink("Extraversion_Reliability_Results.txt")
print(results)
sink()

# Optional: Save the results object for later use
saveRDS(results, file = "Extraversion_Reliability_Results.rds")

# Print confirmation
cat("\nAnalysis complete. Results saved to:\n")
cat("- Extraversion_Reliability_Results.txt (text summary)\n")
cat("- Extraversion_Reliability_Results.rds (R object)\n")