import pandas as pd
import numpy as np
import json

def cronbach_alpha(items_scores):
    """Calcula o coeficiente Alfa de Cronbach."""
    items_scores = np.array(items_scores)
    item_vars = items_scores.var(axis=0, ddof=1)
    total_var = items_scores.sum(axis=1).var(ddof=1)
    n_items = items_scores.shape[1]
    return (n_items / (n_items - 1)) * (1 - item_vars.sum() / total_var)
    

# Carregar os dados do questionário
df = pd.read_csv("Psycho50.csv")

# Carregar o mapeamento de domínios
with open("bfi2facets.json", "r") as f:
    bfi_data = json.load(f)
bfi_items = bfi_data["BFI-2"]["items"]

# Estruturar os domínios do Big Five
domains = {"Open_Mindedness": [], "Conscientiousness": [], "Extraversion": [], "Agreeableness": [], "Negative_Emotionality": []}  # Abertura, Conscienciosidade, Extroversão, Amabilidade, Neuroticismo

for item in bfi_items:
    if item["reversed"]:
        df[str(item["id"])] = 6 - df[str(item["id"])]  # Assumindo escala 1-5

for item in bfi_items:
    domain = item.get("domain")
    if domain in domains:
        domains[domain].append(item["id"])

print(len(df.columns.tolist()))
cols = df.columns.tolist()

# Calcular as métricas para cada domínio

results = {}
for domain, item_ids in domains.items():
    # Filtrar apenas os itens presentes no DataFrame
    valid_items = [item for item in item_ids if str(item) in cols]
    print(valid_items)
    
    if not valid_items:
        print(f"Nenhum item válido encontrado para o domínio {domain}")
        continue
    
    # Obter os scores dos itens
    item_scores = df[[str(item) for item in valid_items]].values
    
    # Calcular Alpha de Cronbach
    alpha = cronbach_alpha(item_scores)
    
    # Calcular variância média dos itens
    variances = np.var(item_scores, axis=0, ddof=1)
    mean_variance = np.mean(variances)
    
    # Calcular covariância média entre itens (excluindo auto-covariâncias)
    cov_matrix = np.cov(item_scores, rowvar=False)
    # Obter apenas as covariâncias entre itens diferentes
    off_diagonal = cov_matrix[np.triu_indices_from(cov_matrix, k=1)]
    mean_covariance = np.mean(off_diagonal) if len(off_diagonal) > 0 else 0
    
    # Armazenar resultados
    results[domain] = {
        "Cronbach's Alpha": alpha,
        "Mean Variance": mean_variance,
        "Mean Covariance": mean_covariance,
        "Number of Items": len(valid_items),
        "Sample Size": len(df)
    }
# Exibir resultados
for domain, metrics in results.items():
    print(f"Domain: {domain}")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")
    print()
