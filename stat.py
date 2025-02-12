import json
import statistics
import sys

def calcular_estatisticas(json_file):
    # Carrega os dados do arquivo JSON
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Extrai os valores de contaInvalid
    conta_invalid_values = [entry["invalid response"] for entry in data.values()]

    # Calcula média, mediana e desvio padrão
    media = statistics.mean(conta_invalid_values)
    mediana = statistics.median(conta_invalid_values)
    desvio_padrao = statistics.stdev(conta_invalid_values)

    # Calcula os quartis
    Q1 = statistics.quantiles(conta_invalid_values, n=4)[0]  # Primeiro quartil
    Q3 = statistics.quantiles(conta_invalid_values, n=4)[2]  # Terceiro quartil

    return media, mediana, desvio_padrao, Q1, Q3

json_file = sys.argv[1]
media, mediana, desvio_padrao, Q1, Q3 = calcular_estatisticas(json_file)

print(f"Média de respostas inválidas: {media:.2f}")
print(f"Mediana de respostas inválidas: {mediana:.2f}")
print(f"Desvio padrão de respostas inválidas: {desvio_padrao:.2f}")
print(f"Primeiro quartil (Q1): {Q1:.2f}")
print(f"Terceiro quartil (Q3): {Q3:.2f}")
