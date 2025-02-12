import pandas as pd
import numpy as np
import json
from scipy.stats import shapiro, kstest, anderson, probplot
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys

def write_report(message, file):
    """Escreve uma mensagem no arquivo de relatório."""
    print(message)  # Para imprimir também na tela
    file.write(message + '\n')  # Escreve no arquivo de relatório

def calculate_domain_scores(data, mapping):
    """
    Calcula as pontuações médias para cada domínio com base no mapeamento JSON.
    """
    domains = {}
    for item in mapping:
        domain = item["domain"]
        item_id = f"{item['id']}"  # Converter ID para string para correspondência
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(item_id)

    # Calcular as médias por domínio
    domain_scores = {}
    for domain, items in domains.items():
        domain_scores[domain] = data[items].mean(axis=1)
    return pd.DataFrame(domain_scores)

def check_normality(data, domain_name, output_dir, report_file):
    """
    Verifica a normalidade para os dados de um domínio usando vários métodos.
    Salva os gráficos no diretório de saída.
    """
    write_report(f"\n=== Analisando normalidade para o domínio: {domain_name} ===", report_file)
    
    # 1. Estatísticas descritivas
    write_report("Estatísticas descritivas:", report_file)
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)
    write_report(f" - Média: {mean:.3f}", report_file)
    write_report(f" - Desvio padrão: {std_dev:.3f}", report_file)
    
    # 2. Testes estatísticos
    write_report("\nTestes estatísticos:", report_file)
    decision = []  # Armazena os resultados dos testes
    
    # Shapiro-Wilk
    stat, p = shapiro(data)
    write_report(f" - Shapiro-Wilk: Estatística={stat:.3f}, p-valor={p:.3f}", report_file)
    decision.append(p > 0.05)
    
    # Kolmogorov-Smirnov
    stat, p = kstest(data, 'norm', args=(mean, std_dev))
    write_report(f" - Kolmogorov-Smirnov: Estatística={stat:.3f}, p-valor={p:.3f}", report_file)
    decision.append(p > 0.05)
    
    # Anderson-Darling
    result = anderson(data, dist='norm')
    write_report(f" - Anderson-Darling: Estatística={result.statistic:.3f}", report_file)
    critical = result.critical_values[2]  # Usando o nível de significância de 5%
    decision.append(result.statistic < critical)
    write_report(f"   Valor crítico para 5%: {critical:.3f}", report_file)

    # Criar diretório para os gráficos, se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # Histograma com curva de densidade
    sns.histplot(data, kde=True)
    plt.title(f"Histograma com Curva de Densidade - {domain_name}")
    plt.xlabel("Pontuações")
    plt.ylabel("Frequência")
    plt.savefig(os.path.join(output_dir, f"{domain_name}_histograma.png"))
    plt.close()
    
    # Gráfico Q-Q
    probplot(data, dist="norm", plot=plt)
    plt.title(f"Gráfico Q-Q - {domain_name}")
    plt.savefig(os.path.join(output_dir, f"{domain_name}_qq_plot.png"))
    plt.close()
    
    # Boxplot
    plt.boxplot(data, vert=False)
    plt.title(f"Boxplot - {domain_name}")
    plt.xlabel("Pontuações")
    plt.savefig(os.path.join(output_dir, f"{domain_name}_boxplot.png"))
    plt.close()
    
    # 4. Decisão final
    write_report("\nDecisão final:", report_file)
    if all(decision):
        write_report(f"Os dados do domínio '{domain_name}' seguem uma distribuição normal com base nos testes estatísticos.", report_file)
    else:
        write_report(f"Os dados do domínio '{domain_name}' não seguem uma distribuição normal com base nos testes estatísticos.", report_file)

# Ler os arquivos
csv_file_path = sys.argv[1]  # Substituir pelo caminho real
json_file_path = 'bfi2facets.json'  # Substituir pelo caminho real
output_directory = 'normality_plotsPsycho'  # Substituir pelo caminho desejado
report_file_path = 'relatorio_normalidadePsycho.txt'  # Caminho do arquivo de relatório

# Carregar os dados
data = pd.read_csv(csv_file_path)
with open(json_file_path, 'r') as f:
    json_data = json.load(f)

# Extrair mapeamento de itens
bfi_items = json_data["BFI-2"]["items"]

# Calcular as pontuações por domínio
domain_scores = calculate_domain_scores(data, bfi_items)

# Criar arquivo de relatório
with open(report_file_path, 'w') as report_file:
    # Escrever cabeçalho no relatório
    write_report("Relatório de Análise de Normalidade", report_file)
    write_report("="*40, report_file)
    
    # Verificar normalidade para cada domínio e salvar os gráficos
    for domain in domain_scores.columns:
        check_normality(domain_scores[domain], domain, output_directory, report_file)

