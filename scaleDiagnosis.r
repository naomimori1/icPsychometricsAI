# Load required libraries
library(psych)
library(ufs) # For scaleDiagnosis function
library(ggplot2)

# Read the data
data <- read.csv("Extraversion.csv", header = TRUE)

# Extract just the item scores (excluding participant IDs)
item_scores <- data[, -1]

# Run scale diagnosis
diagnosis <- scaleDiagnosis(
  dat = item_scores,
  plotSize = 200,          # Size of the output plot
  sizeMultiplier = 1.2,    # Adjusts element sizes in plot
  scaleStructure.ci = TRUE, # Compute confidence intervals
  conf.level = 0.95,       # 95% confidence level
    omega.psych = TRUE,      # Include omega from psych package
)

# Print results to console
print(diagnosis)

# Save results to files
saveRDS(diagnosis, "extraversion_diagnosis_results.rds")

# Save the scattermatrix plot separately
ggsave("extraversion_scattermatrix.png", 
       plot = diagnosis$scatterMatrix$output$scatterMatrix,
       width = 10, height = 8, dpi = 300)

# Print confirmation
cat("\nAnalysis complete. Results saved to:\n")
cat("- Console output with reliability statistics\n")
cat("- extraversion_diagnosis_results.rds (complete analysis object)\n")
cat("- extraversion_scattermatrix.png (visual diagnostics plot)\n")