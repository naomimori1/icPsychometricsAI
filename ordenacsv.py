import pandas as pd

def reorder_columns(input_file, output_file):
    """
    Reordena as colunas de um arquivo CSV gerado anteriormente, organizando as colunas de 1 a 60.
    
    Args:
    - input_file (str): Caminho do arquivo CSV de entrada.
    - output_file (str): Caminho do arquivo CSV de saída com as colunas reordenadas.
    """
    # Lê o arquivo CSV
    data = pd.read_csv(input_file)

    # Mantém a coluna "teste" como a primeira
    base_columns = ["teste"]

    # Gera a lista das colunas numéricas em ordem de 1 a 60 como strings
    score_columns = [str(i) for i in range(1, 61)]

    # Verifica se todas as colunas de 1 a 60 estão presentes
    missing_columns = [col for col in score_columns if col not in data.columns]
    if missing_columns:
        print(f"Colunas ausentes no arquivo: {missing_columns}")
        return

    # Reordena as colunas
    ordered_columns = base_columns + score_columns
    reordered_data = data[ordered_columns]

    # Salva o arquivo com as colunas ordenadas
    reordered_data.to_csv(output_file, index=False)
    print(f"Arquivo com colunas ordenadas salvo em: {output_file}")

# Caminhos dos arquivos
input_file = "combined_FeriasScores.csv"
output_file = "combined_FeriasScores_ordered.csv"

# Executa o processo
reorder_columns(input_file, output_file)

