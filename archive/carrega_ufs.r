# Carregar pacotes necessários
install.packages("psych")
library (psych)
install.packages("readr")
library(readr)
install.packages("jsonlite")
install.packages("dplyr")
library(jsonlite)
library(psych)
library(ufs)
library(GGally)

# Ler os dados do questionário
df <- read.csv("Psycho50.csv")

# Verificar se o dataframe foi carregado corretamente
if (nrow(df) == 0) {
  stop("O arquivo Psycho50.csv está vazio ou não foi carregado corretamente.")
}

# Ler o arquivo de metadados
meta <- fromJSON("bfi2facets.json")

# Verificar se o arquivo JSON foi carregado corretamente
if (is.null(meta$`BFI-2`) || is.null(meta$`BFI-2`$items)) {
  stop("O arquivo bfi2facets.json não contém os dados esperados.")
}

# Organizar itens por domínio
dominios <- split(meta$`BFI-2`$items, meta$`BFI-2`$items$domain)

# Verificar se os domínios foram criados corretamente
if (length(dominios) == 0) {
  stop("Nenhum domínio foi encontrado no arquivo JSON.")
}

# Verificar se o dataframe contém os itens necessários
itens_necessarios <- unlist(lapply(dominios, function(d) {
  paste0("X", d$id)
}))

# Exibir os itens necessários para depuração
cat("Itens necessários:", paste(itens_necessarios, collapse = ", "), "\n")

# Corrigir nomes dos itens para bater com as colunas do df
itens_por_dominio <- lapply(dominios, function(d) {
  paste0("X", d$id)
})

# Verificar se todos os itens realmente existem no dataframe
if (!all(unlist(itens_por_dominio) %in% names(df))) {
  itens_faltantes <- setdiff(unlist(itens_por_dominio), names(df))
  stop("Alguns itens do JSON não correspondem aos nomes das colunas no dataframe. Itens faltantes: ", 
       paste(itens_faltantes, collapse = ", "))
}

# Reverter a pontuação de itens que precisam ser invertidos
ids_reversos <- meta$`BFI-2`$items$id[meta$`BFI-2`$items$reversed == TRUE]
itens_reversos <- paste0("X", ids_reversos)

# Verificar se os itens reversos existem no dataframe
if (!all(itens_reversos %in% names(df))) {
  itens_reversos_faltantes <- setdiff(itens_reversos, names(df))
  stop("Alguns itens reversos não existem no dataframe. Itens faltantes: ", 
       paste(itens_reversos_faltantes, collapse = ", "))
}

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
