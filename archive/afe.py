import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from factor_analyzer import FactorAnalyzer, calculate_kmo
from scipy.stats import bartlett

def cronbach_alpha(items):
    """Calcula o Alpha de Cronbach para um conjunto de itens."""
    item_vars = items.var(axis=0, ddof=1)
    total_var = items.sum(axis=1).var(ddof=1)
    n_items = items.shape[1]
    return (n_items / (n_items - 1)) * (1 - item_vars.sum() / total_var)

# Carregar os dados
df = pd.read_csv("Psycho50.csv")

# Carregar informações sobre os itens do BFI-2
with open("bfi2facets.json", "r") as f:
    bfi2_info = json.load(f)["BFI-2"]["items"]

# Criar um dicionário com os itens organizados por domínio e verificar quais são reversos
domain_items = {}
for item in bfi2_info:
    domain = item["domain"]
    item_id = f"{item['id']}"
    if domain not in domain_items:
        domain_items[domain] = []
    domain_items[domain].append((item_id, item["reversed"]))

# Inverter os itens reversos (assumindo escala de 1 a 5)
for items in domain_items.values():
    for item_id, is_reversed in items:
        if is_reversed and item_id in df.columns:
            df[item_id] = 6 - df[item_id]

# Criar uma matriz apenas com as respostas dos itens do BFI-2
item_columns = [f"{item['id']}" for item in bfi2_info]
df_items = df[item_columns].dropna()  # Remover respostas incompletas

# Verificar adequação para AFE com KMO e Bartlett
kmo_all, kmo_model = calculate_kmo(df_items)
chi_square_value, p_value = bartlett(*df_items.T.values)

print(f"KMO (deve ser > 0.6): {kmo_model:.3f}")
print(f"Teste de Bartlett (p deve ser < 0.05): {p_value:.3f}")

# Calcular autovalores para determinar o número de fatores
fa = FactorAnalyzer(n_factors=df_items.shape[1], rotation=None)
fa.fit(df_items)
ev, v = fa.get_eigenvalues()

# Plotar Scree Plot
plt.figure(figsize=(8, 5))
plt.plot(range(1, len(ev)+1), ev, marker="o", linestyle="--")
plt.axhline(y=1, color="r", linestyle="-")
plt.xlabel("Número de Fatores")
plt.ylabel("Autovalores")
plt.title("Scree Plot")
plt.show()

# Escolher número de fatores baseado no Scree Plot (ex: 5 fatores)
n_fatores = 5
fa = FactorAnalyzer(n_factors=n_fatores, rotation="varimax")
fa.fit(df_items)

# Criar DataFrame com as cargas fatoriais
loadings = pd.DataFrame(fa.loadings_, index=item_columns, columns=[f"Fator {i+1}" for i in range(n_fatores)])

# Ordenar os itens por domínio
item_order = sorted(bfi2_info, key=lambda x: x["domain"])
ordered_index = [str(item["id"]) for item in item_order]
loadings = loadings.loc[ordered_index]


# Determinar o fator dominante para cada item (aquele com maior carga absoluta)
loadings["Fator Dominante"] = loadings.abs().idxmax(axis=1)

# Associar cada item ao seu domínio
item_domains = {item["id"]: item["domain"] for item in bfi2_info}
loadings["Domínio"] = loadings.index.map(item_domains)

# Contar quantos itens de cada domínio carregam em cada fator
domain_factor_counts = pd.crosstab(loadings["Domínio"], loadings["Fator Dominante"])

# Exibir a tabela de associação
print(domain_factor_counts)

# Calcular o Alpha para cada fator
alpha_scores = {}
for fator in loadings["Fator Dominante"].unique():
    fator_itens = loadings[loadings["Fator Dominante"] == fator].index
    alpha_scores[fator] = cronbach_alpha(df_items[fator_itens])

# Exibir resultados
for fator, alpha in alpha_scores.items():
    print(f"{fator}: Alpha de Cronbach = {alpha:.3f}")

# Visualizar cargas fatoriais em um mapa de calor
plt.figure(figsize=(10, 8))
sns.heatmap(loadings, annot=True, cmap="coolwarm", center=0)
plt.title("Cargas Fatoriais Ordenadas por Domínio")
plt.show()
