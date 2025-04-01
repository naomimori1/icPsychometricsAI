import pandas as pd
import numpy as np
import json
import random
from scipy.stats import pearsonr
from itertools import combinations
from numpy.linalg import eigvals

def load_data(csv_path, json_path):
    """Carrega os dados do CSV e as informações do questionário do JSON."""
    try:
        df = pd.read_csv(csv_path)
        with open(json_path, 'r') as f:
            bfi2_info = json.load(f)["BFI-2"]["items"]
        for item in bfi2_info:
            if item["reversed"]:
                df[str(item["id"])] = 6 - df[str(item["id"])]  # Assumindo escala 1-5
        return df, bfi2_info
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Erro ao carregar arquivos: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Erro ao decodificar JSON: {e}")
    except KeyError as e:
        raise KeyError(f"Estrutura do JSON não contém a chave esperada: {e}")

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
    
    # Cria cópia para não alterar a lista original
    shuffled_items = random.sample(items, len(items))
    
    half = len(shuffled_items) // 2
    part1 = sum(df[item[0]].fillna(0) for item in shuffled_items[:half])
    part2 = sum(df[item[0]].fillna(0) for item in shuffled_items[half:half*2])
    
    # Remove linhas com todos os valores faltantes
    valid_data = df[[item[0] for item in shuffled_items]].dropna(how='all')
    if len(valid_data) < 3:
        return np.nan
    
    r, _ = pearsonr(part1, part2)
    return (2 * r) / (1 + r) if not np.isnan(r) else np.nan

def cronbach_alpha(df, items):
    """Calcula o coeficiente Alpha de Cronbach."""
    if len(items) < 2:
        return np.nan
    
    item_scores = np.array([df[item[0]] for item in items if item[0] in df.columns])
    if item_scores.size == 0:
        return np.nan
    
    item_variances = np.var(item_scores, axis=1, ddof=1)
    total_scores = np.sum(item_scores, axis=0)
    total_variance = np.var(total_scores, ddof=1)
    
    if total_variance == 0:
        return np.nan
    
    k = len(item_scores)
    return (k / (k - 1)) * (1 - np.sum(item_variances) / total_variance)

def omega_mcdonald(df, items):
    """Calcula o coeficiente Omega de McDonald (hierárquico)."""
    if len(items) < 2:
        return np.nan
    
    item_scores = np.array([df[item[0]] for item in items if item[0] in df.columns])
    if item_scores.size == 0:
        return np.nan
    
    # Remove observações com valores faltantes
    item_scores = item_scores[:, ~np.isnan(item_scores).any(axis=0)]
    if item_scores.shape[1] < 3:  # Mínimo 3 observações
        return np.nan
    
    cov_matrix = np.cov(item_scores)
    total_variance = np.sum(cov_matrix)
    
    if total_variance == 0:
        return np.nan
    
    eigenvalues = np.real(eigvals(cov_matrix))
    first_eigenvalue = max(eigenvalues)
    return first_eigenvalue / total_variance

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
        
        try:
            results[domain] = {
                "Average Inter-Correlation": average_inter_correlation(df, valid_items),
                "Split-Half Reliability": split_half_reliability(df, valid_items),
                "Cronbach's Alpha": cronbach_alpha(df, valid_items),
                "McDonald's Omega": omega_mcdonald(df, valid_items),
                "Number of Items": len(valid_items),
                "Sample Size": len(df.dropna(subset=[item[0] for item in valid_items]))
            }
        except Exception as e:
            print(f"Erro ao calcular métricas para {domain}: {str(e)}")
            results[domain] = {
                "Average Inter-Correlation": np.nan,
                "Split-Half Reliability": np.nan,
                "Cronbach's Alpha": np.nan,
                "McDonald's Omega": np.nan,
                "Number of Items": len(valid_items),
                "Sample Size": len(df.dropna(subset=[item[0] for item in valid_items]))
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