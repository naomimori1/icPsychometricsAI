import pandas as pd
import numpy as np
import json
import random
from scipy.stats import pearsonr
from itertools import combinations
from numpy.linalg import eigvals
from factor_analyzer import FactorAnalyzer

def load_data(csv_path, json_path):
    """Carrega os dados do CSV e as informações do questionário do JSON."""
    df = pd.read_csv(csv_path)
    with open(json_path, 'r') as f:
        bfi2_info = json.load(f)["BFI-2"]["items"]

    return df, bfi2_info

def process_data(df, bfi2_info):
    """Processa os dados, invertendo itens quando necessário e organizando por domínio."""
    domain_items = {}
    
    # Organiza itens por domínio
    for item in bfi2_info:
        domain = item["domain"]
        item_id = str(item['id'])
        if domain not in domain_items:
            domain_items[domain] = []
        domain_items[domain].append((item_id, item["reversed"]))
    
    # Inverte itens quando necessário
    for domain, items in domain_items.items():
        for item_id, is_reversed in items:
            if item_id in df.columns:
                if is_reversed:
                    # Verifica se os dados estão na escala 1-5 antes de inverter
                    if df[item_id].min() >= 1 and df[item_id].max() <= 5:
                        df[item_id] = 6 - df[item_id]
                    else:
                        raise ValueError(f"Item {item_id} fora da escala esperada 1-5")
    
    return df, domain_items

def average_inter_correlation(df, items):
    """Calcula a correlação média entre todos os pares de itens."""
    if len(items) < 2:
        return np.nan
    
    correlations = []
    for (item1, _), (item2, _) in combinations(items, 2):
        if item1 in df.columns and item2 in df.columns:
            # Remove pares com valores faltantes para o cálculo de correlação
            valid_pairs = df[[item1, item2]].dropna()
            if len(valid_pairs) >= 3:  # Mínimo 3 observações para pearsonr
                r, _ = pearsonr(valid_pairs[item1], valid_pairs[item2])
                correlations.append(r)
    
    return np.mean(correlations) if correlations else np.nan

def split_half_reliability(df, items):
    """Calcula a confiabilidade split-half com correção de Spearman-Brown."""
    if len(items) < 2:
        return np.nan
    
    # Embaralha e divide os itens ao meio
    shuffled_items = random.sample(items, len(items))
    half = len(shuffled_items) // 2
    
    part1_items = [item[0] for item in shuffled_items[:half]]
    part2_items = [item[0] for item in shuffled_items[half:half * 2]]
    
    # Calcula a média dos escores de cada metade
    part1 = df[part1_items].mean(axis=1, skipna=True)
    part2 = df[part2_items].mean(axis=1, skipna=True)
    
    # Remove valores ausentes
    valid_data = pd.concat([part1, part2], axis=1).dropna()
    if len(valid_data) < 3:
        return np.nan
    
    r, _ = pearsonr(valid_data.iloc[:, 0], valid_data.iloc[:, 1])
    return (2 * r) / (1 + r) if not np.isnan(r) else np.nan

def cronbach_alpha(df, items):
    """Calcula o coeficiente Alfa de Cronbach."""
    if len(items) < 2:
        return np.nan

    # Extrai os escores dos itens do DataFrame
    item_scores = np.array([df[item[0]] for item in items if item[0] in df.columns]).T  # Transposta para alinhar com a nova função

    if item_scores.size == 0:
        return np.nan

    # Calcula o Alfa de Cronbach conforme a nova definição
    item_vars = item_scores.var(axis=0, ddof=1)
    total_var = item_scores.sum(axis=1).var(ddof=1)
    n_items = item_scores.shape[1]

    if total_var == 0:
        return np.nan

    return (n_items / (n_items - 1)) * (1 - item_vars.sum() / total_var)



def omega_mcdonald(df, items):
    """Calcula o coeficiente Ômega Hierárquico (\(\omega_h\)) corretamente."""
    if len(items) < 2:
        return np.nan

    item_scores = np.array([df[item[0]].values for item in items if item[0] in df.columns]).T
    if item_scores.size == 0:
        return np.nan

    # Calcula matriz de correlação
    corr_matrix = np.corrcoef(item_scores, rowvar=False)

    # Verifica se a matriz de correlação é positiva definida
    if np.any(eigvals(corr_matrix) <= 0):
        return np.nan

    fa = FactorAnalyzer(n_factors=1, method='ml', rotation=None)
    fa.fit(corr_matrix)
    loadings = fa.loadings_
    general_factor_variance = np.sum(loadings**2)
    total_variance = np.sum(np.diag(corr_matrix))

    # Calcula Omega_h
    omega_h = general_factor_variance / total_variance if total_variance > 0 else np.nan

    return omega_h

def analyze_reliability(csv_path, json_path):
    """Executa a análise completa de confiabilidade para todos os domínios."""
    random.seed(42)  # Para reprodutibilidade
    
    df, bfi2_info = load_data(csv_path, json_path)
    df, domain_items = process_data(df, bfi2_info)
    
    results = {}
    for domain, items in domain_items.items():
        # Filtra apenas itens presentes no DataFrame
        valid_items = [item for item in items if item[0] in df.columns]
        if len(valid_items) < 2:
            print(f"Aviso: Domínio {domain} tem menos de 2 itens válidos. Ignorando.")
            continue

        results[domain] = {
            "Average Inter-Correlation": average_inter_correlation(df, valid_items),
            "Split-Half Reliability": split_half_reliability(df, valid_items),
            "Cronbach's Alpha": cronbach_alpha(df, valid_items),
            "McDonald's Omega": omega_mcdonald(df, valid_items)
        }
    return results

if __name__ == "__main__":
    try:
        results = analyze_reliability("Psycho50.csv", "bfi2facets.json")
        
        print("\nResultados da Análise de Confiabilidade:\n")
        for domain, metrics in results.items():
            print(f"Domínio: {domain}")
            for metric, value in metrics.items():
                if isinstance(value, (int, np.integer)):
                    print(f"  {metric}: {value}")
                elif isinstance(value, float):
                    print(f"  {metric}: {value:.3f}")
            print()
            
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")