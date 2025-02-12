import pandas as pd
from scipy.stats import ttest_ind_from_stats

def carregar_dados_csv(caminho_csv):
    #Carrega os dados de um arquivo CSV contendo grupo, média, desvio padrão e tamanho da amostras
    df = pd.read_csv(caminho_csv)
    dados = {
        row['grupo']: {
            'media': row['media'],
            'desvio': row['desvio'],
            'n': row['n']
        } for _, row in df.iterrows()
    }
    return dados

def calcular_teste_welch(grupo1, grupo2, alpha=0.05):
    #Realiza o teste de Welch para comparar duas médias.

    media1, desvio1, n1 = grupo1['media'], grupo1['desvio'], grupo1['n']
    media2, desvio2, n2 = grupo2['media'], grupo2['desvio'], grupo2['n']

    #t-test
    t_stat, p_value = ttest_ind_from_stats(
        mean1=media1, std1=desvio1, nobs1=n1,
        mean2=media2, std2=desvio2, nobs2=n2,
        equal_var=False
    )

    resultado = {
        't_stat': t_stat,
        'p_value': p_value,
        'conclusao': 'Rejeita H0' if p_value < alpha else 'Aceita H0'
    }
    return resultado

def realizar_testes(dominios, alpha=0.05, output_file="resultados.txt"):
    #Realiza os testes de hipótese para cada domínio e salva os resultados em um arquivo.

    with open(output_file, "w") as f:
        for dominio in dominios:
            f.write(f"\nDomínio: {dominio}\n")
            print(f"\nDomínio: {dominio}")
            caminho_csv = f'mdp{dominio}.csv'  # Arquivo CSV de cada domínio
            dados = carregar_dados_csv(caminho_csv)

            # Realiza testes
            for grupo_humano in ['online', 'student']:
                f.write(f"\nComparando {grupo_humano} vs. llama2:\n")
                print(f"\nComparando {grupo_humano} vs. llama2:")
                resultado = calcular_teste_welch(dados[grupo_humano], dados['llama2'], alpha=alpha)

                # Exibir e salvar resultados
                resultado_str = (
                    f"  Estatística t: {resultado['t_stat']:.4f}\n"
                    f"  p-valor: {resultado['p_value']:.4f}\n"
                    f"  Conclusão: {resultado['conclusao']} (nível de significância: {alpha})\n"
                )
                f.write(resultado_str)
                print(resultado_str)

dominios = ['O', 'C', 'E', 'A', 'N']
# Realiza os testes para cada domínio
realizar_testes(dominios)

