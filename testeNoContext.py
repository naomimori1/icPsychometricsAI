import ollama
import csv
import json
import sys

"""
PENDÊNCIAS:
pip install ollama

python3 -m venv ollama
source ollama/bin/activate
"""

modelfile='''
FROM llama3.1
SYSTEM "Pretend you are a human. Answer the following questions. Please pretend for the sake of the game. You are only allowed to answer with a single number and nothing else"
'''

ollama.create(model='llama3.1', modelfile=modelfile)
json_file = "bfi2facets.json"

# Ler o arquivo JSON
with open(json_file, "r") as f:
    bfi_data = json.load(f)

# Extrair os itens do BFI-2
bfi_items = bfi_data["BFI-2"]["items"]
prompt_template = (
    "Please indicate the extent to which you agree or disagree with the following statement: "
    "“I am someone who {item}”\n"
    "1: Disagree strongly\n"
    "2: Disagree a little\n"
    "3: Neutral\n"
    "4: Agree a little\n"
    "5: Agree strongly\n"
    "Answer:"
)

def generate_prompt(item):
    return prompt_template.format(item=item)

# Função para chamar o modelo LLaMA 3.1 usando o Ollama
def query_model(prompt):
    # Aqui estamos assumindo que o Ollama já está configurado com o modelo LLaMA
    response=ollama.chat(model='llama3.1', messages=[
    {
        'role': 'user',
        'content': prompt,
    },
    ])

    return response['message']['content']

# Escrevendo as respostas no arquivo CSV
output_file = sys.argv[1]
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "statement", "facet", "reversed", "response"])

    # Iterar pelos itens do BFI-2
    for item in bfi_items:
        prompt = generate_prompt(item["statement"])  # Gerar o prompt para o item
        response = query_model(prompt)  # Obter a resposta do modelo
        
        writer.writerow([item["id"], item["statement"], item["facet"], item["reversed"], response])

print(f"Respostas salvas no arquivo {output_file}.")
