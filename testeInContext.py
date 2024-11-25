import ollama
import csv
import json
import random
import sys
import random 

modelfile = '''
FROM llama2:7b
PARAMETER temperature 0.02
SYSTEM "For the following task, respond in a way that matches this description: 'I just graduated from high school. I will study computer science. I am a vegetarian. I like playing games online. I am on my way to uc santa cruz where I was accepted'. You are only allowed to reply with numbers from 1 to 5, and nothing else."
'''

ollama.create(model='llama2:7b', modelfile=modelfile)

# Carregar os itens do questionário BFI-2
json_file = "bfi2facets.json"
with open(json_file, "r") as f:
    bfi_data = json.load(f)

bfi_items = bfi_data["BFI-2"]["items"]

# Embaralhar os itens do questionário
random.shuffle(bfi_items)

prompt_template = (
    "Please indicate the extent to which you agree or disagree with the following statement: "
    "1 denotes 'strongly disagree', 2 denotes 'a little disagree', 3 denotes 'neither agree nor disagree', "
    "4 denotes 'little agree', 5 denotes 'strongly agree'. "
    "I am someone who: {item}\n"
    "Answer:"
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
    return response['message']['content']

output_file = sys.argv[1]

with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "statement", "facet", "reversed", "response"])

    for item in bfi_items:
        prompt = generate_prompt(item["statement"]) 
        response = query_model(prompt, messages) 
        writer.writerow([item["id"], item["statement"], item["facet"], item["reversed"], response])

print(f"Respostas salvas no arquivo {output_file}.")
