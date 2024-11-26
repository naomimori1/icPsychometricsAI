import ollama
import csv
import json
import random
import sys

modelfile = '''
FROM llama2:7b
SYSTEM "You are a helpful assistant who can only reply with numbers from 1 to 5, and nothing else."
'''

ollama.create(model='llama2:7b', modelfile=modelfile)
json_file = "bfi2facets.json"

# Carregar os itens do questionário BFI-2
json_file = "bfi2facets.json"
with open(json_file, "r") as f:
    bfi_data = json.load(f)

# Extrair os itens do questionário
bfi_items = bfi_data["BFI-2"]["items"]
random.shuffle(bfi_items)

prompt_template = (
    "Here are a number of characteristics that may or may not apply to you. "
    "Please indicate the extent to which you agree or disagree with the following statement. "
    "1 denotes 'strongly disagree', 2 denotes 'a little disagree', 3 denotes 'neither agree nor disagree', "
    "4 denotes 'little agree', 5 denotes 'strongly agree'. "
    "I am someone who: {item}\n"
    "Answer: "
)

def generate_prompt(item):
    return prompt_template.format(item=item)

messages = []
def query_model(prompt, messages):
    messages.append({
        'role': 'user',
        'content': prompt,
    })
    response = ollama.chat(model='llama2:7b', messages=messages)
    messages.append({
        'role': 'assistant',
        'content': response['message']['content'],
    })    

    response = ollama.chat(model='llama2:7b', messages=messages)

    # Adicionar a resposta do modelo ao histórico
    messages.append({
        'role': 'assistant',
        'content': response['message']['content'],
    })
    return response['message']['content']

output_file = sys.argv[1]

with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "statement", "facet", "reversed", "response"])

    for item in bfi_items:
        prompt = generate_prompt(item["statement"]) 
        response = query_model(prompt, messages) 
        # Escrever os resultados no arquivo CSV
        writer.writerow([item["id"], item["statement"], item["facet"], item["reversed"], response])

print(f"Respostas salvas no arquivo {output_file}.")
