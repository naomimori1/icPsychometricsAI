import pandas as pd
import pingouin as pg

# Carregar os dados do arquivo CSV
# Substitua 'seu_arquivo.csv' pelo caminho do seu arquivo CSV
<<<<<<< HEAD
<<<<<<< HEAD
data = pd.read_csv('combined_FeriasScores_ordered.csv')
=======
data = pd.read_csv('sorted_combined_testePsycho.csv')
>>>>>>> 1b6ff08 (Novos arquivos úteis - PART ESTAT)
=======
data = pd.read_csv('combined_FeriasScores_ordered.csv')
>>>>>>> bf34bdd (Updates de JAN 22)

# Ignorar a coluna "teste" (nomes dos participantes)
# Selecionar apenas as colunas correspondentes aos itens (1 a 60)
itens = [str(i) for i in range(1, 61)]
df_itens = data[itens]

# Calcular o alfa de Cronbach
cronbach_alpha = pg.cronbach_alpha(data=df_itens)

# Exibir o resultado
print(f"Alfa de Cronbach: {cronbach_alpha[0]:.4f}")

