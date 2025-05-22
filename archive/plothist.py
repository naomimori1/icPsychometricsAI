import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np

# Carregar dados do arquivo JSON
with open("bfi2facets.json", "r") as f:
    bfi2_data = json.load(f)

# Criar um mapeamento de colunas para domínios
domain_mapping = {}
for item in bfi2_data["BFI-2"]["items"]:
    domain_mapping[item["id"]] = item["domain"]

# Carregar o arquivo CSV
csv_file = "Psycho1to50.csv"
df = pd.read_csv(csv_file)

# Ordenar as linhas corretamente
df = df.sort_values(by="teste", key=lambda x: x.str.extract(r'(\d+)')[0].astype(int))

# Criar um dicionário para armazenar os scores por domínio
domain_scores = {domain: [] for domain in set(domain_mapping.values())}

# Agrupar os valores por domínio
for col in df.columns[1:]:  # Ignorar a primeira coluna "teste"
    item_id = int(col)  # Converter nome da coluna para número
    if item_id in domain_mapping:
        domain = domain_mapping[item_id]
        domain_scores[domain].extend(df[col].dropna().tolist())

# Criar histogramas para cada domínio
for domain, scores in domain_scores.items():
    plt.figure(figsize=(8, 5))
    plt.hist(scores, bins=np.arange(1, 7)-0.5, edgecolor='black', alpha=0.7)
    plt.xticks(range(1, 6))
    plt.xlabel("Score")
    plt.ylabel("Frequência")
    plt.title(f"Histograma de {domain}")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# Criar tabelas de frequência para cada domínio
for domain, items in item_scores.items():
    print(f"\nTabela de Frequência - {domain}")
    table = pd.DataFrame(items).fillna(0).astype(int)
    print(table)

# Plotar distribuição de dados por domínio
plt.figure(figsize=(10, 6))
for domain, scores in domain_scores.items():
    plt.hist(scores, bins=np.arange(1, 7)-0.5, alpha=0.5, label=domain, edgecolor='black')
plt.xticks(range(1, 6))
plt.xlabel("Score")
plt.ylabel("Frequência")
plt.title("Distribuição de Scores por Domínio")
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

