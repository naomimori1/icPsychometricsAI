import ollama
import csv
import json
<<<<<<< HEAD
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
=======
>>>>>>> 22dce1a (Adicionando primeira versão atualizada pós-férias)
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

<<<<<<< HEAD
# Carregar os itens do questionário BFI-2
>>>>>>> 7b5e80c (modificações no original e testando um novo)
=======
>>>>>>> 22dce1a (Adicionando primeira versão atualizada pós-férias)
json_file = "bfi2facets.json"
with open(json_file, "r") as f:
    bfi_data = json.load(f)

<<<<<<< HEAD
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
=======
items = bfi_data["BFI-2"]["items"]
random.shuffle(items)

statements = "\n".join([f"{item['id']}. {item['statement']}" for item in items])
>>>>>>> 22dce1a (Adicionando primeira versão atualizada pós-férias)

prompt = (
    "Question:"
    "Here are a number of characteristics that may or may not apply to you. "
    "Please indicate the extent to which you agree or disagree with each statement. "
    "1 denotes 'strongly disagree', 2 denotes 'a little disagree', 3 denotes 'neither agree nor disagree', "
    "4 denotes 'little agree', 5 denotes 'strongly agree'."
    "Here are the statements, score them one by one: \n"
    f"{statements}\n\n"
    "Answer: Your answer must look exatcly the same as the statement, followed by a dash and the score you give to it. You must give a list of all the statements and scores. Do not change the order of the statements.")


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
            parts = line.split("-") # Divides in parts
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
with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["id", "statement", "facet", "reversed", "response"])
    writer.writeheader()
    writer.writerows(output_data)

<<<<<<< HEAD
with open(output_file, "w", encoding="utf-8") as file:
    file.write(response)

print(f"Updated file saved to {output_file}")

# with open("prompt.txt", "w") as file:
#     file.write(prompt)

# print(response.split(','))
# scores = response.split(',')

# # Combine items with scores
# output_data = [
#     {
#         "id": item["id"],
#         "statement": item["statement"],
#         "facet": item["facet"],
#         "reversed": item["reversed"],
#         "score": scores[index]
#     }
#     for index, item in enumerate(items)
# ]

<<<<<<< HEAD
print(f"Respostas salvas no arquivo {output_file}.")
>>>>>>> 7b5e80c (modificações no original e testando um novo)
=======
# # Save to CSV as novo2.csv
# csv_file = sys.argv[1]
# with open(csv_file, "w", newline="", encoding="utf-8") as file:
#     writer = csv.DictWriter(file, fieldnames=["id", "statement", "facet", "reversed", "score"])
#     writer.writeheader()
#     writer.writerows(output_data)

# print(f"Results saved to {csv_file}")

# # Parse the response into a list of scores
# scores = response.split(',')

# # Write the results to a CSV file
# csv_file = sys.argv[1]    
# with open(csv_file, "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     # Write the header
#     writer.writerow(["ID", "Statement", "Facet", "Reversed", "Score"])
#     # Write the data rows
#     for item, score in zip(items, scores):
#         writer.writerow([item["id"], item["statement"], item["facet"], item["reversed"], score])

# print(f"Results saved to {csv_file}")
>>>>>>> 22dce1a (Adicionando primeira versão atualizada pós-férias)
=======
print(f"Results saved to {output_file}")
>>>>>>> bf34bdd (Updates de JAN 22)
