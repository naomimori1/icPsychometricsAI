import pandas as pd
import numpy as np
import json
from scipy.stats import pearsonr
from itertools import combinations
from numpy.linalg import eigvals

def load_data(csv_path, json_path):
    df = pd.read_csv(csv_path)
    with open(json_path, 'r') as f:
        bfi2_info = json.load(f)["BFI-2"]["items"]
    return df, bfi2_info

def process_data(df, bfi2_info):
    domain_items = {}
    for item in bfi2_info:
        domain = item["domain"]
        item_id = f"{item['id']}"
        if domain not in domain_items:
            domain_items[domain] = []
        domain_items[domain].append((item_id, item["reversed"]))
    
    for domain, items in domain_items.items():
        for item_id, is_reversed in items:
            if is_reversed:
                df[item_id] = 6 - df[item_id]  # Inverte escala (assumindo escala de 1 a 5)
    return df, domain_items

def average_inter_correlation(df, items):
    correlations = []
    for (item1, _), (item2, _) in combinations(items, 2):
        r, _ = pearsonr(df[item1], df[item2])
        correlations.append(r)
    return np.mean(correlations) if correlations else 0

def split_half_reliability(df, items):
    np.random.shuffle(items)
    half = len(items) // 2
    part1 = sum(df[item[0]] for item in items[:half])
    part2 = sum(df[item[0]] for item in items[half:])
    r, _ = pearsonr(part1, part2)
    return 2 * r / (1 + r) if not np.isnan(r) else 0

def cronbach_alpha(df, items):
    item_scores = np.array([df[item[0]] for item in items])
    item_variances = np.var(item_scores, axis=1, ddof=1)
    total_variance = np.var(np.sum(item_scores, axis=0), ddof=1)
    k = len(items)
    return (k / (k - 1)) * (1 - sum(item_variances) / total_variance)

def omega_mcdonald(df, items):
    item_scores = np.array([df[item[0]] for item in items])
    cov_matrix = np.cov(item_scores)
    total_variance = np.sum(cov_matrix)
    first_eigenvalue = max(eigvals(cov_matrix))
    omega = first_eigenvalue / total_variance if total_variance > 0 else 0
    return omega

def analyze_reliability(csv_path, json_path):
    df, bfi2_info = load_data(csv_path, json_path)
    df, domain_items = process_data(df, bfi2_info)
    results = {}
    for domain, items in domain_items.items():
        avg_corr = average_inter_correlation(df, items)
        split_half = split_half_reliability(df, items)
        alpha = cronbach_alpha(df, items)
        omega = omega_mcdonald(df, items)
        results[domain] = {
            "Average Inter-Correlation": avg_corr,
            "Split-Half Reliability": split_half,
            "Cronbach's Alpha": alpha,
            "McDonald's Omega": omega
        }
    return results

if __name__ == "__main__":
    results = analyze_reliability("Psycho50.csv", "bfi2facets.json")
    for domain, metrics in results.items():
        print(f"{domain}:")
        for metric, value in metrics.items():
            print(f"  {metric}: {value:.3f}")
        print()
