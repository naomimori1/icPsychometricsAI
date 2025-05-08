# Load required libraries
library(psych)
library(ufs) # For scaleDiagnosis function
library(ggplot2)
library(gridExtra)
library(nortest)  # For Anderson-Darling test

#' This code performs an analysis on a dataframe corresponding to one of the domains of the BFI-2 personality inventory, passed as an argument. 
#' It begins by analyzing the structure of the dataframe using functions from the `ufs` package. 
#' Subsequently, it computes the Mega analysis using the `psych` package directly. 
#' A normality assessment is then conducted using the `ufs` package. 
#' Throughout the program, relevant files and plots are generated and saved for further use or visualization.
#' 
#' @param filename The name of the CSV file containing the data (without the .csv extension).
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
print(head(item_scores)) # Check the first few rows of item scores
items <- colnames(item_scores)
print(items) # Check the item names


# Print a line indicating the start of scale structure analysis
cat("\n\n=== Scale Structure Analysis ===\n")
results <- scaleStructure(
  data = item_scores,
  digits = 3,          # Number of decimal places to display
  ci = TRUE,           # Compute confidence intervals
  conf.level = 0.95,   # 95% confidence intervals
  omega.psych = TRUE,  # Include omega from psych package
  poly = TRUE          # Compute ordinal reliability estimates
)

# Save results to a text file and print to console
sink(paste0(tools::file_path_sans_ext(basename(filename)), "_Reliability_Results.txt"), split = TRUE)
print(results)
sink() # Properly close the sink

cat("\n\n=== Scale Structure Analysis Complete ===\n")
# Run scale diagnosis
diagnosis <- scaleDiagnosis(
  data = item_scores,
  scaleReliability.ci = TRUE # Compute confidence intervals
)

# Save the results to a text file and print to console
sink(paste0(tools::file_path_sans_ext(basename(filename)), "_diagnosis.txt"), split = TRUE)
print(diagnosis)
sink() # Properly close the sink

# Save the scattermatrix plot separately
ggsave(paste0(tools::file_path_sans_ext(basename(filename)), "_scattermatrix.png"), 
  plot = diagnosis$scatterMatrix$output$scatterMatrix,
  width = 10, height = 8, dpi = 300)

# Print confirmation
cat("\nAnalysis complete. Results saved to:\n")
cat("- ", paste0(tools::file_path_sans_ext(basename(filename)), "_diagnosis.txt"), " (text summary)\n")
cat("- ", paste0(tools::file_path_sans_ext(basename(filename)), "_scattermatrix.png"), " (scatter matrix plot)\n")

cat("\n\n=== Omega Assessment using psych package directly ===\n")
resultado_omega <- omega(item_scores, nfactors = 1, plot = TRUE)

# 4. Exibir os resultados
print(resultado_omega)

# 5. Salvar os resultados em um arquivo
sink("resultados_omegaE.txt")
print(resultado_omega)
sink()

# 6. Salvar o gráfico do omega
png("omega_plot.png", width = 800, height = 600)
omega(item_scores, nfactors = 1, plot = TRUE)
dev.off()

# Mensagem de confirmação
cat("Análise concluída. Resultados salvos em:\n")
cat("- Console (visualização imediata)\n")
cat("- resultados_omega.txt (arquivo de texto)\n")
cat("- omega_plot.png (gráfico do modelo omega)\n")

all_scores <- unlist(data[, -1])
cat("\n\n=== Normality Assessment for ALL Participants Combined ===\n")
result_all <- normalityAssessment(all_scores, samples = 10000, digits = 3)

# Explicitly print results and plots
print(result_all)  # Isso mostrará estatísticas + plots no console

# Se quiser salvar também em arquivo (opcional)
sink("Extraversion_NormalityResults.txt")
print(result_all)
sink()