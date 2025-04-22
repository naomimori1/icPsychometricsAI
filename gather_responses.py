import os
import subprocess
import json
import sys

'''
FUNCIONAMENTO:
    python3 gather_responses.py <prefixo do arquivo CSV> <arquivo de saída JSON>

    O script processa arquivos CSV com o prefixo especificado, executando o script scores.py
    para cada arquivo. Os resultados são armazenados em um arquivo JSON de saída.

    Atualmente, está processando no diretório atual.
'''

csv_folder = os.getcwd()

results = {}
arquivos = sys.argv[1]

csv_files = [f'{arquivos}{num}.csv' for num in range(1, 51)]
for csv_file in csv_files:
    csv_path = os.path.join(csv_folder, csv_file)
    
    file_id = os.path.splitext(csv_file)[0]
    
    # Verifica se o arquivo existe
    try:
        # Executa o script scores.py e captura a saída
        result = subprocess.check_output(['python3', 'scores.py', csv_path], text=True)
        
        lines = result.strip().split('\n')
        contaInvalid = int(lines[0])
        
        # Extrai os scores dos domínios
        domain_scores = {}
        for line in lines[2:]:  # Pula a segunda linha ("Scores de cada domínio:")
            domain, score = line.split(': ')
            domain_scores[domain.strip()] = float(score)
        
        # Adiciona os scores ao dicionário usando o nome do arquivo como ID
        results[file_id] = {
            "invalid response": contaInvalid,
            "e": domain_scores.get('BFI2_Extraversion'),
            "a": domain_scores.get('BFI2_Agreeableness'),
            "c": domain_scores.get('BFI2_Conscientiousness'),
            "n": domain_scores.get('BFI2_Neuroticism'),
            "o": domain_scores.get('BFI2_Openness')
        }
    
    except subprocess.CalledProcessError as e:
        print(f"Erro ao processar {csv_file}: {e}")
    except Exception as ex:
        print(f"Erro inesperado com {csv_file}: {ex}")

sorted_results = dict(sorted(results.items(), key=lambda item: int(item[0].split(arquivos)[-1])))
output_file = sys.argv[2]
with open(output_file, 'w') as json_file:
    json.dump(sorted_results, json_file, indent=4)

print(f"Resultados salvos em {output_file}")
