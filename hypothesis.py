import pandas as pd
from scipy.stats import f

def carregar_dados_csv(caminho_csv):
    """
    Carrega os dados de um arquivo CSV contendo grupo, média, desvio padrão e tamanho da amostra.

    Args:
        caminho_csv (str): Caminho para o arquivo CSV.

    Returns:
        dict, dict: Dicionários com as variâncias e tamanhos das amostras por grupo.
    """
    # Ler o CSV
    df = pd.read_csv(caminho_csv)
    
    # Verificar se as colunas esperadas existem
    colunas_esperadas = {'grupo', 'desvio', 'n'}
    if not colunas_esperadas.issubset(df.columns):
        raise ValueError(f"O arquivo CSV deve conter as colunas: {colunas_esperadas}")
    
    # Criar dicionários de variâncias e tamanhos
    variancias = {row['grupo']: row['desvio'] ** 2 for _, row in df.iterrows()}
    tamanhos = {row['grupo']: row['n'] for _, row in df.iterrows()}
    
    return variancias, tamanhos

def testar_variancias_por_dominio(variancias, tamanhos, alpha=0.05):
    """
    Testa a homogeneidade das variâncias entre grupos para cada domínio do BFI-2.

    Args:
        variancias (dict): Variâncias para cada grupo e domínio.
                           Exemplo: {"o": {"online": var_online, "student": var_student, "modelo": var_modelo}, ...}.
        tamanhos (dict): Tamanhos das amostras para cada grupo.
                         Exemplo: {"online": n_online, "student": n_student, "modelo": n_modelo}.
        alpha (float): Nível de significância (default: 0.05).

    Returns:
        None. Imprime os resultados do teste.
    """
    print("Teste de Homogeneidade das Variâncias para Cada Domínio")
    print("-" * 70)

    for dominio, grupo_variancias in variancias.items():
        # Ordenar variâncias por valor
        variancias_ordenadas = sorted(grupo_variancias.items(), key=lambda x: x[1])
        menor_grupo, menor_var = variancias_ordenadas[0]
        maior_grupo, maior_var = variancias_ordenadas[-1]

        # Calcular o valor F
        F = maior_var / menor_var

        # Graus de liberdade
        df1 = tamanhos[maior_grupo] - 1
        df2 = tamanhos[menor_grupo] - 1

        # Valor crítico de F
        F_critico = f.ppf(1 - alpha, df1, df2)

        # Avaliar o resultado
        resultado = "Aceitável" if F <= F_critico else "Não aceitável"

        # Imprimir resultados
        print(f"Domínio: {dominio.upper()}")
        print(f"  Maior Grupo: {maior_grupo}, Variância = {maior_var:.4f}, N = {tamanhos[maior_grupo]}")
        print(f"  Menor Grupo: {menor_grupo}, Variância = {menor_var:.4f}, N = {tamanhos[menor_grupo]}")
        print(f"  F = {F:.4f}, F crítico = {F_critico:.4f}")
        print(f"  Resultado: {resultado}")
        print("-" * 70)


# Caminho dos arquivos CSV para cada domínio (substitua com os caminhos reais)
dominios = ['O', 'C', 'E', 'A', 'N']  # Exemplo de domínios: O, C, E, A, N

# Para cada domínio, carregar os dados dos arquivos CSV e realizar os testes
for dominio in dominios:
    caminho_csv = f'mdp{dominio}.csv'  # Arquivo CSV de cada domínio
    try:
        variancias, tamanhos = carregar_dados_csv(caminho_csv)
        # Realizar o teste de homogeneidade das variâncias para o domínio
        testar_variancias_por_dominio({dominio: variancias}, tamanhos)
    except Exception as e:
        print(f"Erro ao processar o domínio {dominio}: {e}")

