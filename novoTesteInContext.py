import ollama
import csv
import json
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

json_file = "bfi2facets.json"
with open(json_file, "r") as f:
    bfi_data = json.load(f)

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
