import os
import subprocess
import json

# Pasta com os arquivos CSV
csv_folder = '.'

# Dicionário para armazenar os resultados
results = {}

# Gera uma lista de arquivos ordenados pelo número no nome
<<<<<<< HEAD
csv_files = [f'testePsycho{num}.csv' for num in range(1, 51)]
=======
csv_files = [f'testePsycho{num}.csv' for num in range(1, 11)]
>>>>>>> 22dce1a (Adicionando primeira versão atualizada pós-férias)

# Percorre os arquivos na ordem correta (de 1 a 40)
for csv_file in csv_files:
    csv_path = os.path.join(csv_folder, csv_file)
    
    # Extrai o número do arquivo para usar como ID
    file_id = os.path.splitext(csv_file)[0]
    
    # Chama o script scores.py para processar o arquivo CSV
    try:
        # Executa o script scores.py e captura a saída
        result = subprocess.check_output(['python3', 'scores.py', csv_path], text=True)
        
        # Extrai a quantidade de respostas inválidas e os scores
        lines = result.strip().split('\n')
        contaInvalid = int(lines[0])  # Primeiro valor da saída é o número de respostas inválidas

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

sorted_results = dict(sorted(results.items(), key=lambda item: int(item[0].split('testePsycho')[-1])))
<<<<<<< HEAD
output_file = 'scoresPsycho50.json'

=======
output_file = 'scoresPsycho.json'
>>>>>>> 22dce1a (Adicionando primeira versão atualizada pós-férias)
with open(output_file, 'w') as json_file:
    json.dump(sorted_results, json_file, indent=4)

print(f"Resultados salvos em {output_file}")

