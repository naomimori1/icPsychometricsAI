import pandas as pd
import json
import pingouin as pg
import seaborn as sns
import matplotlib.pyplot as plt

# Caminhos dos arquivos
csv_file = 'sorted_combined_testePsycho.csv'  # Substitua pelo caminho do arquivo CSV
json_file = 'bfi2facets.json'  # Substitua pelo caminho do arquivo JSON

# Carregar o JSON da estrutura do BFI-2
with open(json_file, 'r') as f:
    bfi_structure = json.load(f)

# Criar mapeamento de domínios e itens reversos
domain_items = {}
reversed_items = {}
for item in bfi_structure["BFI-2"]["items"]:
    domain = item["facet"]
    if domain not in domain_items:
        domain_items[domain] = []
    domain_items[domain].append(str(item["id"]))
    if item["reversed"]:
        reversed_items[str(item["id"])] = True

# Carregar os dados do CSV e remover a coluna "teste"
data = pd.read_csv(csv_file)
data_numeric = data.drop(columns=['teste'])  # Apenas dados numéricos

# Ajustar itens reversos (6 - resposta, pois Likert varia de 1 a 5)
for item_id in reversed_items:
    if item_id in data_numeric.columns:
        data_numeric[item_id] = 6 - data_numeric[item_id]

# Cálculo do alfa de Cronbach e análise de correlação para cada domínio
results = {}
for domain, items in domain_items.items():
    if not all(item in data_numeric.columns for item in items):
        print(f"Aviso: Alguns itens do domínio {domain} não estão presentes nos dados.")
        continue

    # Filtrar os dados do domínio
    domain_data = data_numeric[items]

    # Calcular o alfa de Cronbach
    alpha, _ = pg.cronbach_alpha(data=domain_data)

    # Calcular a matriz de correlação
    correlation_matrix = domain_data.corr()

    # Visualizar matriz de correlação como gráfico de calor
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", cbar=True)
    plt.title(f"Matriz de Correlação: {domain}")
    plt.show()

    # Armazenar resultados
    results[domain] = {
        "alpha": alpha,
        "correlation_matrix": correlation_matrix
    }

# Exibir resultados dos alfas
print("Resultados do Alfa de Cronbach por Domínio:")
for domain, res in results.items():
    print(f"Domínio: {domain}, Alfa de Cronbach: {res['alpha']:.4f}")

