import pandas as pd
import json

# Carrega dados
df = pd.read_csv("Psycho50.csv")
with open("bfi2facets.json", "r") as f:
    data = json.load(f)

# Organiza itens por domínio
dominios = {}
reverse = {}

for item in data["BFI-2"]["items"]:
    id_str = str(item["id"])
    dom = item["domain"]
    dominios.setdefault(dom, []).append(id_str)
    reverse[id_str] = item["reversed"]

# Aplica reversão onde necessário
for col in df.columns[1:]:  # ignora a coluna de ID
    if reverse.get(col):
        df[col] = 6 - df[col]

# Salva um CSV por domínio
for dom, itens in dominios.items():
    df[[df.columns[0]] + itens].to_csv(f"{dom}.csv", index=False)
