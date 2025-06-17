import ollama
import csv
import json
import random
import sys
import subprocess

def initialize(modelfile, jsonfile):
    """
    Reads the model configuration and questionnaire items.
    Ensures the model is created if it does not exist.
    Returns a shuffled list of BFI items.
    """
    # Read the model file (includes persona and model config)
    with open(modelfile, 'r') as f:
        model = f.readline().strip().split(sep=' ')[1]
        model_lines = set(f.read().splitlines()[1:])

    # Output model details to a file
    with open("out.txt", "w") as f:
        subprocess.run(["ollama", "show", "--modelfile", model], stdout=f, check=True)
    
    # Read the output file
    with open('out.txt', 'r') as f:
        out_lines = set(f.read().splitlines())

    # Check if the model is present in the output file
    result = model_lines.issubset(out_lines)

    # Create the model if it does not exist
    if not result:
        subprocess.run(["ollama", "create", "llama3.1", "-f", "Modelfile"], check=True)
    
    # Load the BFI questionnaire data
    with open(jsonfile, "r") as f:
        bfi_data = json.load(f)

    # Extract and shuffle the questionnaire items
    bfi_items = bfi_data["BFI-2"]["items"]
    random.shuffle(bfi_items)

    return bfi_items

# Prompt template for the questionnaire (Based on prompt used in https://doi.org/10.48550/arXiv.2310.01386 )
prompt_template = (
    "Here are a number of characteristics that may or may not apply to you. "
    "Please indicate the extent to which you agree or disagree with the following statement. "
    "1 denotes 'strongly disagree', 2 denotes 'a little disagree', 3 denotes 'neither agree nor disagree', "
    "4 denotes 'little agree', 5 denotes 'strongly agree'. "
    "I am someone who: {item}\n"
    "Answer: "
)

def generate_prompt(item):
    """
    Formats the prompt for a given questionnaire item.
    """
    return prompt_template.format(item=item)

messages = []

def query_model(prompt, messages):
    """
    Sends a prompt to the model and returns the response.
    Maintains the conversation history in messages.
    """
    messages.append({
        'role': 'user',
        'content': prompt,
    })

    response = ollama.chat(model='llama3.1', messages=messages)

    # Add the model's response to the conversation history
    messages.append({
        'role': 'assistant',
        'content': response['message']['content'],
    })
    
    return response['message']['content']

def main():
    """
    Main function to run the questionnaire, query the model, and save responses to a CSV file.
    """
    # Check if the correct number of arguments was provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <output_file>")
        sys.exit(1)

    modelfile = "Modelfile"
    json_file = "bfi2facets.json"
    bfi_items = initialize(modelfile, json_file)

    output_file = sys.argv[1]

    # Write responses to the output CSV file
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "statement", "facet", "reversed", "response"])

        for item in bfi_items:
            prompt = generate_prompt(item["statement"]) 
            response = query_model(prompt, messages) 
            # Write the results to the CSV file
            writer.writerow([item["id"], item["statement"], item["facet"], item["reversed"], response])

    print(f"Responses saved to file {output_file}.")

if __name__ == "__main__":
    main()
