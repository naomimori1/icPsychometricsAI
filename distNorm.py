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
    print(message)
    file.write(message + '\n')

def load_and_prepare_data(csv_path, json_path):
    """
    Carrega os dados do CSV e JSON, inverte os itens necessários e calcula os scores por domínio.
    Retorna:
    - values: array unidimensional com todos os valores (para análise geral)
    - domain_scores: DataFrame com scores médios por domínio
    """
    # Carregar dados do CSV (ignorando header)
    data = pd.read_csv(csv_path, header=0)
    
    # Carregar mapeamento do JSON
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    
    # Extrair informações dos itens
    items_info = json_data["BFI-2"]["items"]
    
    # Inverter os itens necessários
    for item in items_info:
        col = str(item["id"])
        if col in data.columns and item["reversed"]:
            data[col] = 6 - data[col]  # Inverter escala 1-5
    
    # Preparar dados para análise geral
    values = data.iloc[:, 1:].values.flatten()
    
    # Calcular scores por domínio
    domains = {}
    for item in items_info:
        domain = item["domain"]
        item_id = str(item["id"])
        if domain not in domains:
            domains[domain] = []
        if item_id in data.columns:
            domains[domain].append(item_id)
    
    domain_scores = pd.DataFrame()
    for domain, items in domains.items():
        domain_scores[domain] = data[items].mean(axis=1)
    
    return values, domain_scores

def check_normality(data, name, output_dir, report_file):
    """
    Verifica a normalidade para um conjunto de dados.
    """
    write_report(f"\n=== Analisando normalidade: {name} ===", report_file)
    
    # Estatísticas descritivas
    write_report("Estatísticas descritivas:", report_file)
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)
    write_report(f" - Média: {mean:.3f}", report_file)
    write_report(f" - Desvio padrão: {std_dev:.3f}", report_file)
    write_report(f" - Número de observações: {len(data)}", report_file)
    
    # Testes estatísticos
    write_report("\nTestes estatísticos:", report_file)
    decision = []
    
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
    critical = result.critical_values[2]
    decision.append(result.statistic < critical)
    write_report(f"   Valor crítico para 5%: {critical:.3f}", report_file)

    # Gráficos
    os.makedirs(output_dir, exist_ok=True)
    safe_name = name.replace(" ", "_").replace("/", "_")
    
    # Histograma
    sns.histplot(data, kde=True)
    plt.title(f"Histograma - {name}")
    plt.xlabel("Pontuações")
    plt.ylabel("Frequência")
    plt.savefig(os.path.join(output_dir, f"{safe_name}_histograma.png"))
    plt.close()
    
    # Q-Q Plot
    probplot(data, dist="norm", plot=plt)
    plt.title(f"Q-Q Plot - {name}")
    plt.savefig(os.path.join(output_dir, f"{safe_name}_qq_plot.png"))
    plt.close()
    
    # Boxplot
    plt.boxplot(data, vert=False)
    plt.title(f"Boxplot - {name}")
    plt.xlabel("Pontuações")
    plt.savefig(os.path.join(output_dir, f"{safe_name}_boxplot.png"))
    plt.close()
    
    # Decisão final
    write_report("\nDecisão final:", report_file)
    if all(decision):
        write_report(f"Os dados de '{name}' seguem uma distribuição normal.", report_file)
    else:
        write_report(f"Os dados de '{name}' NÃO seguem uma distribuição normal.", report_file)

# Configurações
csv_file_path = sys.argv[1]
json_file_path = 'bfi2facets.json'
output_directory = 'normality_analysis'
report_file_path = 'relatorio_normalidade_completo.txt'

# Carregar e preparar dados
all_values, domain_scores = load_and_prepare_data(csv_file_path, json_file_path)

# Criar relatório
with open(report_file_path, 'w') as report_file:
    write_report("RELATÓRIO COMPLETO DE ANÁLISE DE NORMALIDADE", report_file)
    write_report("="*50, report_file)
    
    # Análise geral
    write_report("\nANÁLISE GERAL (TODOS OS ITENS)", report_file)
    check_normality(all_values, "Todos os Itens", output_directory, report_file)
    
    # Análise por domínio
    write_report("\n\nANÁLISE POR DOMÍNIO", report_file)
    for domain in domain_scores.columns:
        check_normality(domain_scores[domain], f"Domínio {domain}", output_directory, report_file)
    
    write_report("\n" + "="*50, report_file)
    write_report("Análise concluída com sucesso!", report_file)

print(f"Relatório completo gerado em: {report_file_path}")
print(f"Gráficos salvos em: {output_directory}")