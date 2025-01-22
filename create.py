import ollama
import csv
import json
import sys

# Define model with system constraints
modelfile = '''
FROM llama2:7b
PARAMETER temperature 0.01
SYSTEM "You are a helpful assistant who can only reply with numbers from 1 to 5, and nothing else."
'''

ollama.create(model='llama2:7b', modelfile=modelfile)
