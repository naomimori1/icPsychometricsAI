import pandas as pd
import os
import sys

'''

FUNCIONAMENTO:
    python3 juntacsv.py <nome do arq de saída>
    atualmente o script trabalha com arquivos que começam com "testePsycho" e terminam
    com "csv", junta todos eles em um outro arquivo csv na forma
    teste, 1, 2, ..., 60
    teste1, 1, 4, ...,5
    teste2, 2,5,...,3

'''

def merge_and_transform_csv(output_file):
    """
    Combina múltiplos arquivos CSV com nomes no padrão 'testPsycho{num}.csv',
    transformando os dados conforme especificado.
    
    Args:
    - output_file (str): Caminho do arquivo CSV de saída.
    """
    merged_data = []  # Lista para armazenar os dados transformados

    # Percorre todos os arquivos no diretório atual com o padrão 'testPsycho{num}.csv'
    for filename in os.listdir("."):
        if filename.startswith("testePsycho") and filename.endswith(".csv"):
            print(f"Lendo o arquivo: {filename}")
            try:
                # Lê o arquivo atual
                data = pd.read_csv(filename)

                # Verifica se as colunas esperadas existem
                if not {"id", "response"}.issubset(data.columns):
                    print(f"Erro: Arquivo {filename} não possui as colunas esperadas ('id' e 'score').")
                    continue

                # Cria um DataFrame temporário com os scores organizados por ID
                transformed = pd.DataFrame({
                    "teste": [filename],
                    **{str(id_): [score] for id_, score in zip(data["id"], data["response"])}
                })

                # Adiciona ao conjunto final de dados
                merged_data.append(transformed)

            except Exception as e:
                print(f"Erro ao processar o arquivo {filename}: {e}")

    # Combina todos os dados transformados em um único DataFrame
    if merged_data:
        final_data = pd.concat(merged_data, ignore_index=True)
        # Preenche colunas ausentes (caso algum arquivo não tenha todas os IDs)
        final_data = final_data.fillna(0)
        # Salva no arquivo de saída
        final_data.to_csv(output_file, index=False)
        print(f"Dados combinados e transformados salvos em: {output_file}")
    else:
        print("Nenhum arquivo foi processado.")

# Nome do arquivo de saída
output_file = sys.argv[1]
merge_and_transform_csv(output_file)

