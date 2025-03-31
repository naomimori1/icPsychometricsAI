import ollama
import csv
import json
import sys
import subprocess

import subprocess

# Executa o comando no terminal
subprocess.run(["ollama", "create", "llama3.1", "-f", "Modelfile"], check=True)

