import ollama
import csv
import json
import random
import sys

<<<<<<< HEAD
=======
# Configuração do modelo Ollama
>>>>>>> 94fc1e4 (Código by my dear friend)
modelfile = '''
FROM llama2:7b
SYSTEM "You are a helpful assistant who can only reply with numbers from 1 to 5 in every statement. Format: \"score\"."
'''

ollama.create(model='llama2:7b', modelfile=modelfile)
<<<<<<< HEAD

json_file = "bfi2facets.json"
=======
>>>>>>> 94fc1e4 (Código by my dear friend)

# Carregar os itens do questionário BFI-2
json_file = "bfi2facets.json"
with open(json_file, "r") as f:
    bfi_data = json.load(f)

<<<<<<< HEAD
=======
# Extrair os itens do questionário
>>>>>>> 94fc1e4 (Código by my dear friend)
bfi_items = bfi_data["BFI-2"]["items"]

# Embaralhar os itens para garantir variabilidade
random.shuffle(bfi_items)

# Template do prompt
prompt_template = (
    "Here are a number of characteristics that may or may not apply to you. "
    "Please indicate the extent to which you agree or disagree with that statement. "
    "1 denotes 'strongly disagree', 2 denotes 'a little disagree', 3 denotes 'neither agree nor disagree', "
    "4 denotes 'little agree', 5 denotes 'strongly agree'. Here are the statements, score them one by one: "
    "I am someone who: {item}"
)

# Função para gerar o prompt para cada item
def generate_prompt(item):
    return prompt_template.format(item=item)

# Lista para rastrear mensagens trocadas com o modelo
messages = []

# Função para consultar o modelo Ollama
def query_model(prompt, messages):
<<<<<<< HEAD
=======
    # Adicionar mensagem do usuário ao histórico
>>>>>>> 94fc1e4 (Código by my dear friend)
    messages.append({
        'role': 'user',
        'content': prompt,
    })
<<<<<<< HEAD
    response = ollama.chat(model='llama2:7b', messages=messages)
    messages.append({
        'role': 'assistant',
        'content': response['message']['content'],
    })    
=======

    # Enviar consulta ao modelo e receber resposta
    response = ollama.chat(model='llama2:7b', messages=messages)

    # Adicionar a resposta do modelo ao histórico
    messages.append({
        'role': 'assistant',
        'content': response['message']['content'],
    })

    # Retornar a resposta do modelo
>>>>>>> 94fc1e4 (Código by my dear friend)
    return response['message']['content']

# Caminho do arquivo de saída (primeiro argumento da linha de comando)
output_file = sys.argv[1]

<<<<<<< HEAD
=======
# Abrir arquivo CSV para salvar as respostas
>>>>>>> 94fc1e4 (Código by my dear friend)
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    # Cabeçalho do arquivo
    writer.writerow(["id", "statement", "facet", "reversed", "response"])

    # Processar cada item do questionário
    for item in bfi_items:
<<<<<<< HEAD
        prompt = generate_prompt(item["statement"]) 
        response = query_model(prompt, messages) 
=======
        # Gerar o prompt com o item atual
        prompt = generate_prompt(item["statement"])

        # Obter resposta do modelo para o prompt
        response = query_model(prompt, messages)

        # Escrever os resultados no arquivo CSV
>>>>>>> 94fc1e4 (Código by my dear friend)
        writer.writerow([item["id"], item["statement"], item["facet"], item["reversed"], response])

print(f"Respostas salvas no arquivo {output_file}.")
