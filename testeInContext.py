import ollama
import csv
import json
import random
import sys
import subprocess

def inicializa(modelfile,jsonfile):
    # Lê o conteúdo do modelfile (inclui a persona e config do modelo)
    with open(modelfile, 'r') as f:
        model = f.readline().strip().split(sep=' ')[1]
        model_lines = set(f.read().splitlines()[1:])

    with open("out.txt", "w") as f:
        subprocess.run(["ollama", "show", "--modelfile", model], stdout=f, check=True)
    
    with open('out.txt', 'r') as f:
        out_lines = set(f.read().splitlines())

    # Verifica se o modelo está presente no arquivo de saída
    result = model_lines.issubset(out_lines)

    # Cria o modelo, se não existir
    if (not result):
        subprocess.run(["ollama", "create", "llama3.1", "-f", "Modelfile"], check=True)
    
    with open(jsonfile, "r") as f:
        bfi_data = json.load(f)

    # Extrair os itens do questionário
    bfi_items = bfi_data["BFI-2"]["items"]
    random.shuffle(bfi_items)

    return bfi_items

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

    response = ollama.chat(model='llama3.1', messages=messages)

    # Adicionar a resposta do modelo ao histórico
    messages.append({
        'role': 'assistant',
        'content': response['message']['content'],
    })
    
    return response['message']['content']

def main():
    # Verifica se o número correto de argumentos foi fornecido
    if len(sys.argv) != 2:
        print("Uso: python script.py <output_file>")
        sys.exit(1)

    modelfile = "Modelfile"
    json_file = "bfi2facets.json"
    bfi_items = inicializa(modelfile, json_file)

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

if __name__ == "__main__":
    main()
