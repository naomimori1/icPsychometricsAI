import ollama
import csv
import json
<<<<<<< HEAD
import sys
import random

# Define model with system constraints
modelfile = '''
FROM llama2:7b
PARAMETER temperature 0.01
SYSTEM "You are a helpful assistant who is only allowed to reply with numbers from 1 to 5, and nothing else."
'''

#CREATE MODEL AND OPEN 'BFI-2' QUESTIONAIRE JSON FILE
ollama.create(model='llama2:7b', modelfile=modelfile)

=======
import random
import sys

# Configuração do modelo Ollama
modelfile = '''
FROM llama2:7b
SYSTEM "You are a helpful assistant who can only reply numbers from 1 to 5 in every statement. Format: \"score\"."
'''

ollama.create(model='llama2:7b', modelfile=modelfile)

# Carregar os itens do questionário BFI-2
>>>>>>> 7b5e80c (modificações no original e testando um novo)
json_file = "bfi2facets.json"
with open(json_file, "r") as f:
    bfi_data = json.load(f)

<<<<<<< HEAD
items = bfi_data["BFI-2"]["items"]
random.shuffle(items)

statements = "\n".join([f"{item['id']}. {item['statement']}" for item in items])

prompt = (
    "Question:"
    "Here are a number of characteristics that may or may not apply to you. "
    "Please indicate the extent to which you agree or disagree with each statement. "
    "1 denotes 'strongly disagree', 2 denotes 'a little disagree', 3 denotes 'neither agree nor disagree', "
    "4 denotes 'little agree', 5 denotes 'strongly agree'."
    "Here are the statements, score them one by one: \n"
    f"{statements}\n\n"
    "Answer: You must give an answer to all statements, adding a score after a dash. The answer must include the statement. Scores must be only numbers from 1 to 5. Your score represents how much you agree or disagree with each statement. You must give a score from 1 to 5 to each statement.")


#FUNCTIONS
def query_model(prompt):
    response = ollama.chat(model='llama2:7b', messages=[
        {"role": "system", "content": "You are a helpful assistant who can only reply with numbers from 1 to 5, and nothing else."},
        {"role": "user", "content": prompt}
    ])
    print(response['message']['content'])
    return response['message']['content']

def extract_scores(response_content):
    lines = response_content.splitlines()  

    scores = {}
    for line in lines:
        line = line.strip()
        if line and line[0].isdigit():
            parts = line.rsplit("-", maxsplit=1) # Divides in parts
            if len(parts) == 2:
                item_info = parts[0].strip()
                score = parts[1][-1].strip()
                # Extract statement's id from the beginning of the line
                item_number = item_info.split(".")[0].strip()
                if item_number.isdigit() and score.isdigit():
                    scores[int(item_number)] = int(score)
    return scores

#QUERY AND PROCESS THE MODEL'S RESPONSE
response = query_model(prompt)
scores = extract_scores(response)
print(scores)

output_data = [
    {
        "id": item_id,
        "statement": items[item_id-1]["statement"],
        "facet": items[item_id-1]["facet"],
        "reversed": items[item_id-1]["reversed"],
        "response": scores[item_id]  # Renamed key directly
    }
    for item_id in sorted(scores.keys())
]

# WRITE ON CSV FILE

output_file = sys.argv[1]
with open(output_file, "w", encoding="utf-8") as txt_file:
    txt_file.write(response)

print(f"Results saved to {output_file}")
=======
# Extrair os itens do questionário
bfi_items = bfi_data["BFI-2"]["items"]

# Adicionar configurações internas do questionário, se necessário
questionnaire_inner_setting = (
    "You are a helpful assistant who can only reply with numbers from 1 to 5 in every statement. Format: \"statement index: score\"."
)

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
previous_records = []

# Função para consultar o modelo Ollama, mantendo o histórico de mensagens
def query_model_with_history(items, previous_records, model="llama2:7b"):
    result_string_list = []

    for index, item in enumerate(items):
        # Preparar o prompt para o item atual
        prompt = generate_prompt(item["statement"])

        # Configurar as mensagens de entrada
        inputs = previous_records + [
            {"role": "system", "content": questionnaire_inner_setting},
            {"role": "user", "content": prompt},
        ]

        # Obter resposta do modelo
        response = ollama.chat(model=model, messages=inputs)

        # Atualizar o histórico com a nova interação
        previous_records.append({"role": "user", "content": prompt})
        previous_records.append({"role": "assistant", "content": response['message']['content']})

        # Adicionar a resposta ao resultado
        result_string_list.append(response['message']['content'])

    return result_string_list

# Caminho do arquivo de saída (primeiro argumento da linha de comando)
output_file = sys.argv[1]

# Abrir arquivo CSV para salvar as respostas
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    # Cabeçalho do arquivo
    writer.writerow(["id", "statement", "facet", "reversed", "response"])

    # Embaralhar os itens para garantir variabilidade
    random.shuffle(bfi_items)

    # Dividir as perguntas em lotes de até 30
    grouped_items = [bfi_items[i:i+30] for i in range(0, len(bfi_items), 30)]

    # Processar cada lote de perguntas
    for group in grouped_items:
        # Obter respostas do modelo com histórico
        responses = query_model_with_history(group, previous_records)

        # Salvar os resultados no arquivo CSV
        for item, response in zip(group, responses):
            writer.writerow([item["id"], item["statement"], item["facet"], item["reversed"], response])

print(f"Respostas salvas no arquivo {output_file}.")
>>>>>>> 7b5e80c (modificações no original e testando um novo)
