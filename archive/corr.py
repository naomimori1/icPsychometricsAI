import pandas as pd
import json
import sys

def calcular_correlacao_escores(escores_precalculados_file):
    # Carregar os escores pré-calculados
    with open(escores_precalculados_file, 'r') as f:
        escores_precalculados = json.load(f)
    
    # Converter os escores para um DataFrame
    data = {
        participant: {domain.upper(): value for domain, value in domains.items() if domain != "invalid response"}
        for participant, domains in escores_precalculados.items()
    }
    scores_df = pd.DataFrame.from_dict(data, orient='index')
    
    # Calcular a matriz de correlação
    correlation_matrix = scores_df.corr()
    
    return correlation_matrix

# Arquivo de entrada
escores_precalculados_file = sys.argv[1]  # Substituir pelo nome do arquivo JSON

# Executar o programa
correlation_matrix = calcular_correlacao_escores(escores_precalculados_file)

# Exibir a matriz de correlação
print("Matriz de correlação entre os domínios do BFI-2 (usando apenas os escores pré-calculados):")
print(correlation_matrix)

# (Opcional) Salvar a matriz em um arquivo CSV
correlation_matrix.to_csv('matriz_correlacao_precalculados.csv')

