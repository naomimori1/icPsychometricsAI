library(jsonlite)
library(readr)
library(psych)
library(dplyr)

# Lendo o CSV
df <- read.csv("Psycho50.csv")

# Lendo o JSON
bfi2_info <- fromJSON("bfi2facets.json")$BFI2$items

# Criando um dicionário de itens por domínio
domain_items <- list()

# Organiza itens por domínio
for (item in bfi2_info) {
  domain <- item$domain
  item_id <- as.character(item$id)
  is_reversed <- item$reversed
  
  if (!domain %in% names(domain_items)) {
    domain_items[[domain]] <- list()
  }
  
  domain_items[[domain]][[item_id]] <- is_reversed
}

# Inverte itens quando necessário
for (domain in names(domain_items)) {
  for (item_id in names(domain_items[[domain]])) {
    is_reversed <- domain_items[[domain]][[item_id]]
    
    if (item_id %in% colnames(df)) {
      if (is_reversed) {
        # Verifica se os dados estão na escala 1-5 antes de inverter
        if (min(df[[item_id]], na.rm = TRUE) >= 1 && max(df[[item_id]], na.rm = TRUE) <= 5) {
          df[[item_id]] <- 6 - df[[item_id]]
        }
      }
    }
  }
}

# Calculando o ômega hierárquico para cada domínio
omega_results <- list()

for (domain in names(domain_items)) {
  domain_vars <- names(domain_items[[domain]])
  domain_data <- df %>% select(all_of(domain_vars)) %>% na.omit()  # Remove NAs
  
  if (ncol(domain_data) > 1) {  # Omega precisa de pelo menos 2 itens
    omega_results[[domain]] <- omega(domain_data)$omega_h
  } else {
    omega_results[[domain]] <- NA  # Se houver apenas um item, não é possível calcular
  }
}

# Exibir os resultados
print(omega_results)

