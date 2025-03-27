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
    domain = item.get("domain")
    if domain in domains:
        domains[domain].append(item["id"])

print(domains)
for domain in domains:
    print(len(domain))
# Calcular as métricas para cada domínio
results = {}
for domain, items in domains.items():
    valid_items = [item for item in items if item in df.columns]
    if valid_items:
        domain_data = df[valid_items].dropna()
        alpha = cronbach_alpha(domain_data)
        mean_variance = domain_data.var(axis=0, ddof=1).mean()
        cov_matrix = domain_data.cov()
        mean_covariance = cov_matrix.where(~np.eye(len(valid_items), dtype=bool)).stack().mean()
        results[domain] = {
            "Cronbach's Alpha": alpha,
            "Mean Variance": mean_variance,
            "Mean Covariance": mean_covariance
        }

# Exibir resultados
for domain, metrics in results.items():
    print(f"Domain: {domain}")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")
    print()
