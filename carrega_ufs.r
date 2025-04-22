# Carregar pacotes necessários
library(jsonlite)
library(ufs)
library(GGally)

# Ler os dados do questionário
df <- read.csv("Psycho50.csv")

# Ler o arquivo de metadados
meta <- fromJSON("bfi2facets.json")

# Organizar itens por domínio
dominios <- split(meta$`BFI-2`$items, meta$`BFI-2`$items$domain)

# Verificar se o dataframe contém os itens necessários
itens_necessarios <- unlist(lapply(dominios, function(d) {
  paste0("X", d$id)
}))

dominios

# Corrigir nomes dos itens para bater com as colunas do df
itens_por_dominio <- lapply(dominios, function(d) {
  paste0("X", d$id)
})

itens_por_dominio
# Verificar se todos os itens realmente existem no dataframe
if (!all(unlist(itens_por_dominio) %in% names(df))) {
  stop("Alguns itens do JSON não correspondem aos nomes das colunas no dataframe.")
}

# Reverter a pontuação de itens que precisam ser invertidos
ids_reversos <- meta$`BFI-2`$items$id[meta$`BFI-2`$items$reversed == TRUE]
itens_reversos <- paste0("X", ids_reversos)

reverter_item <- function(x) {
  return(6 - x)
}

df[itens_reversos] <- lapply(df[itens_reversos], reverter_item)

cat("Itens com pontuação revertida:", paste(itens_reversos, collapse = ", "), "\n")

# Análise de estrutura de escala por domínio
resultados_structure <- lapply(names(itens_por_dominio), function(nome_dom) {
  cat("\n\n--- Estrutura de Escala:", nome_dom, "---\n\n")
  scaleStructure(
    data = df,
    items = itens_por_dominio[[nome_dom]],
    ci = TRUE,
    omega.psych = TRUE,
  )
})
names(resultados_structure) <- names(itens_por_dominio)

# Análise de diagnóstico de escala por domínio
resultados_diagnostico <- lapply(names(itens_por_dominio), function(nome_dom) {
  cat("\n\n--- Diagnóstico de Escala:", nome_dom, "---\n\n")
  scaleDiagnosis(
    data = df,
    items = itens_por_dominio[[nome_dom]]
  )
})
names(resultados_diagnostico) <- names(itens_por_dominio)

# Exemplo: acesso a resultados de um domínio específico
resultados_structure$Agreeableness
resultados_diagnostico$Agreeableness
