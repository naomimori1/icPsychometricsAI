#!/bin/bash

# Lista de strings
strings=("Extraversion" "Conscientiousness" "Open_Mindedness" "Agreeableness" "Negative_Emotionality")

# Caminho para o script R
ufs_script="ufsAnalysis.r"

# Verifica se o script R existe
if [[ ! -f $ufs_script ]]; then
    echo "Erro: O script $ufs_script não foi encontrado."
    exit 1
fi

# Itera sobre cada elemento da lista e executa o script R
for elemento in "${strings[@]}"; do
    echo "Executando $ufs_script com o elemento: $elemento"
    Rscript "$ufs_script" "$elemento"
    if [[ $? -ne 0 ]]; then
        echo "Erro ao executar $ufs_script com o elemento: $elemento"
        exit 1
    fi
done

echo "Execução concluída com sucesso."