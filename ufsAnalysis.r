# Load required libraries

library(psych)
library(ufs)
library(ggplot2)
library(gridExtra)
library(nortest)  # For Anderson-Darling test

#' This code performs an analysis on a dataframe corresponding to one of the
#' domains of the BFI-2 personality inventory, passed as an argument.  # nolint
#' It begins by analyzing the structure of the dataframe using functions from the `ufs` package.  # nolint
#' Subsequently, it computes the Mega analysis using the `psych` package directly.  # nolint
#' A normality assessment is then conducted using the `ufs` package.
#' Throughout the program, relevant files and plots are generated
#'  and saved for further use or visualization.
#'
#' @param filename The name of the CSV file containing the data
#' (without the .csv extension).
#' @return None
#' @examples
#' # To run the analysis, use the command line:
#' Rscript ufsAnalysis.r Extraversion
#' #' # This will read the file "Extraversion.csv" and perform the analysis.
#'

args <- commandArgs(trailingOnly = TRUE)
if (length(args) == 0) {
  stop("Please provide the filename as a command-line argument.")
}
filename <- args[1]

# Read the data
data <- read.csv(paste0(filename, ".csv"), header = TRUE)

# Extract just the item scores (excluding participant IDs)
item_scores <- data[, -1]

# --------------------- START OF ANALYSIS ---------------------

cat("\n\n=== Scale Structure Analysis ===\n")
results <- scaleStructure(
  data = item_scores,
  digits = 3,
  ci = TRUE,
  conf.level = 0.95,   # 95% confidence intervals
  omega.psych = TRUE,  # Include omega from psych package
  poly = TRUE          # Compute ordinal reliability estimates
)

# Save results to a text file and print to console
sink(paste0(tools::file_path_sans_ext(basename(filename)),
            "_Reliability_Results.txt"), split = TRUE)
print(results)
sink() # Properly close the sink

cat("\n\n=== Scale Structure Analysis Complete ===\n")
# Run scale diagnosis
diagnosis <- scaleDiagnosis(
  data = item_scores,
  scaleReliability.ci = TRUE # Compute confidence intervals
)

# Save the results to a text file and print to console
sink(paste0(tools::file_path_sans_ext(basename(filename)),
            "_diagnosis.txt"), split = TRUE)
print(diagnosis)
sink() # Properly close the sink

# Print confirmation
cat("\nAnalysis complete. Results saved to:\n")
cat("- ", paste0(tools::file_path_sans_ext(basename(filename)),
                 "_diagnosis.txt"), " (text summary)\n")
cat("- ", paste0(tools::file_path_sans_ext(basename(filename)),
                 "_scattermatrix.png"), " (scatter matrix plot)\n")

cat("\n\n=== Omega Assessment using psych package directly ===\n")
resultado_omega <- omega(item_scores, nfactors = 1, plot = TRUE)

#  Print the omega results to console
print(resultado_omega)

# Save the omega results to a text file
sink(paste0(tools::file_path_sans_ext(basename(filename)),
            "_omega_results.txt"))
print(resultado_omega)
sink()

# Save the omega plot
png(paste0(tools::file_path_sans_ext(basename(filename)),
           "_omega_plot.png"), width = 800, height = 600)
omega(item_scores, nfactors = 1, plot = TRUE)
dev.off()

# Print confirmation
cat("Análise de Omega usando psych concluída.\n")
all_scores <- unlist(data[, -1], use.names = FALSE)
cat("\n\n=== Normality Assessment for ALL Participants Combined ===\n")
result_all <- normalityAssessment(all_scores, samples = 10000, digits = 3)

#Save normality plots
png(paste0(tools::file_path_sans_ext(basename(filename)),
           "_normality_plots.png"), width = 10, height = 8, units = "in",
    res = 300)
grid.arrange(
  result_all$plot.sampleDist,
  result_all$plot.samplingDist,
  result_all$qqPlot.sampleDist,
  result_all$qqPlot.samplingDist,
  ncol = 2
)
dev.off()

# Explicitly print results and plots
print(result_all)  # Isso mostrará estatísticas + plots no console

# Se quiser salvar também em arquivo (opcional)
sink(paste0(tools::file_path_sans_ext(basename(filename)),
            "_NormalityResults.txt"))
print(result_all)
sink()