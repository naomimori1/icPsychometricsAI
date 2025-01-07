import json
import statistics
import sys

<<<<<<< HEAD
"""
mdp.py recebe um argumento que corresponde ao arquivo json contendo os scores de cada execução.
"""
=======
>>>>>>> 22dce1a (Adicionando primeira versão atualizada pós-férias)
def calcular_estatisticas(json_file):
    # Carrega os dados do arquivo JSON
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Dicionário para armazenar os valores dos domínios
    dominios = {
        'o': [],
        'c': [],
        'e': [],
        'a': [],
        'n': []
    }
    
    for entrada in data.values():
        for dominio in dominios:
            dominios[dominio].append(entrada[dominio])
    
    # Calcula e exibe média e desvio padrão para cada domínio
    for dominio, valores in dominios.items():
        media = statistics.mean(valores)
        desvio_padrao = statistics.stdev(valores) if len(valores) > 1 else 0
        print(f"Domínio {dominio.upper()}:")
        print(f"  Média: {media:.2f}")
        print(f"  Desvio padrão: {desvio_padrao:.2f}")

if __name__ == "__main__":
    json_file = sys.argv[1]
    calcular_estatisticas(json_file)

