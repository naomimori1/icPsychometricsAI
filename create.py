import ollama
import csv
import json
import sys

# Define model with system constraints
modelfile = '''
FROM llama2:7b
PARAMETER temperature 0.01
SYSTEM "You are a helpful assistant who can only reply with numbers from 1 to 5, and nothing else. Format: \"statement index: score\"."
'''

ollama.create(model='llama2:7b', modelfile=modelfile)

with open("prompt.txt", "r") as prompt_file:
    prompt = prompt_file.read().strip()
    
response = ollama.generate(model='llama2:7b', prompt=prompt)
    
print("Raw Response Object:", response)

# Parse the response to extract the content (if necessary)
response_content = response['text'] if 'text' in response else response

# Save the prompt and response to a CSV file
output_file = "responses.csv"

# Write to CSV
with open(output_file, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    # Write the header
    writer.writerow(["Prompt", "Response"])
    # Write the data
    writer.writerow([prompt, response_content])

# Print the final parsed response content
print(f"Response saved to {output_file}: {response_content}")

