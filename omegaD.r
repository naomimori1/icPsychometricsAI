# Carregar a biblioteca necessária
library(psych)

# 1. Ler os dados do arquivo CSV
dados <- read.csv("Extraversion.csv", header = TRUE)

# 2. Selecionar apenas os itens (excluir a coluna de identificação)
itens <- dados[, -1]

# 3. Calcular o ômega de McDonald
resultado_omega <- omega(itens, nfactors = 1, plot = TRUE)

# 4. Exibir os resultados
print(resultado_omega)

# 5. Salvar os resultados em um arquivo
sink("resultados_omegaE.txt")
print(resultado_omega)
sink()

# 6. Salvar o gráfico do omega
png("omega_plot.png", width = 800, height = 600)
omega(itens, nfactors = 1, plot = TRUE)
dev.off()

# Mensagem de confirmação
cat("Análise concluída. Resultados salvos em:\n")
cat("- Console (visualização imediata)\n")
cat("- resultados_omega.txt (arquivo de texto)\n")
cat("- omega_plot.png (gráfico do modelo omega)\n")