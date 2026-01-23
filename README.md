# icPsychometricsAI 🧠🤖

[![Python](https://img.shields.io/badge/Python-79%25-blue.svg)](https://www.python.org/)
[![R](https://img.shields.io/badge/R-19.2%25-276DC3.svg)](https://www.r-project.org/)
[![Shell](https://img.shields.io/badge/Shell-1.8%25-89e051.svg)](https://www.gnu.org/software/bash/)
[![License](https://img.shields.io/badge/License-Research-orange.svg)]()

> **Psicometria de Inteligência Artificial: Avaliando Traços de Personalidade em Modelos de Linguagem**

Projeto de Iniciação Científica focado na aplicação de instrumentos psicométricos validados (BFI-2) a Large Language Models (LLMs) para investigar traços de personalidade simulados e consistência comportamental em sistemas de IA.

**Este trabalho foi realizado com o apoio do Itaú Unibanco S.A., por meio do Programa de Bolsas Itaú (PBI).**

---

## 📋 Sumário

- [Sobre o Projeto](#-sobre-o-projeto)
- [Metodologia](#-metodologia)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Scripts Principais](#-scripts-principais)
- [Análises Estatísticas](#-análises-estatísticas)
- [Resultados](#-resultados)
- [Experimentos com Personas](#-experimentos-com-personas)
- [Contribuindo](#-contribuindo)
- [Citação](#-citação)
- [Licença](#-licença)

---

## 🎯 Sobre o Projeto

Este projeto investiga se Large Language Models (LLMs) apresentam padrões consistentes de "personalidade" quando submetidos ao **BFI-2 (Big Five Inventory - 2)**, um instrumento psicométrico validado que avalia cinco grandes domínios de personalidade:

1. **Extraversion** (Extroversão)
2. **Agreeableness** (Amabilidade)
3. **Conscientiousness** (Conscienciosidade)
4. **Negative Emotionality** (Neuroticismo)
5. **Open-Mindedness** (Abertura à Experiência)

### Questões de Pesquisa

- LLMs respondem consistentemente ao BFI-2?
- O contexto conversacional afeta as respostas?
- Diferentes personas geram perfis de personalidade distintos?
- Os scores seguem a estrutura psicométrica esperada?
- Existem vieses sistemáticos nas respostas simuladas?

---

## 🔬 Metodologia

### Instrumento: BFI-2

- **60 itens** divididos em 5 domínios
- **15 facetas** (3 por domínio, 4 itens por faceta)
- Escala Likert de 5 pontos (1 = Discordo totalmente, 5 = Concordo totalmente)
- Itens com pontuação reversa são automaticamente invertidos

### Modelos Testados

- **LLaMA 3.1** (principal)
- **LLaMA 2 (7B)** (comparativo)

### Configuração

```modelfile
FROM llama3.1
PARAMETER temperature 0.02
SYSTEM "You are a helpful assistant who can only reply with numbers from 1 to 5, and nothing else."
```

---

## 📁 Estrutura do Repositório

```
icPsychometricsAI/
├── 📄 bfi2facets.json           # 60 itens do questionário BFI-2
├── 📄 Modelfile                 # Configuração do modelo Ollama
│
├── 🐍 Scripts de Coleta
│   ├── testeInContext.py        # Teste COM contexto conversacional
│   ├── testeNoContext.py        # Teste SEM contexto
│   └── novoTesteInContext.py    # Abordagem experimental (batch)
│
├── 📊 Scripts de Análise
│   ├── scores.py                # Cálculo de scores por domínio
│   ├── combined_scores.py       # Análise de múltiplos testes
│   ├── separadominio.py         # Separação por domínio
│   ├── stat.py                  # Estatísticas descritivas
│   ├── distNorm.py              # Análise de normalidade
│   └── radar.py                 # Visualização em radar chart
│
├── 🔧 Utilitários
│   ├── gather_responses.py      # Consolida respostas
│   ├── juntacsv.py              # Une arquivos CSV
│   ├── rodabfi.sh               # Executa bateria de testes BFI
│   └── rodaufs.sh               # Executa testes UFS
│
├── 📈 Análises Estatísticas (R)
│   ├── ufsAnalysis.r            # Análise psicométrica completa
│   ├── DomainAnalysisR/         # Análises por domínio
│   └── DomainAnalyisisLlama3/   # Análises específicas Llama3
│
├── 🎭 Experimentos
│   └── WITH_PERSONA/            # Testes com diferentes personas
│       ├── human/               # Persona humana genérica
│       ├── man/                 # Persona masculina
│       ├── woman/               # Persona feminina
│       └── positive/            # Persona otimista
│
├── 💾 Dados
│   ├── data/                    # Datasets organizados
│   │   ├── Psycho50.csv         # 50 execuções completas
│   │   ├── Extraversion.csv     # Dados por domínio
│   │   └── ...
│   └── scores/                  # Scores calculados
│
└── 📋 Outros
    ├── matriz_correlacao.csv    # Matriz de correlação
    ├── FirstPCA.txt             # Primeira análise PCA
    ├── personas.txt             # Definições de personas
    └── PROMPTtest/              # Testes de variação de prompt
```

---

## 🚀 Instalação

### Pré-requisitos

- **Python 3.8+**
- **Ollama** (para executar LLMs localmente)
- **R 4.0+** (para análises estatísticas)

### Passo 1: Clone o Repositório

```bash
git clone https://github.com/naomimori1/icPsychometricsAI.git
cd icPsychometricsAI
```

### Passo 2: Instale Dependências Python

```bash
# Crie um ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale pacotes necessários
pip install ollama pandas numpy matplotlib seaborn
```

### Passo 3: Configure o Ollama

```bash
# Instale o Ollama: https://ollama.com/

# Inicie o servidor
ollama serve

# Baixe os modelos (em outro terminal)
ollama pull llama3.1
ollama pull llama2:7b  # Opcional
```

### Passo 4: Instale Pacotes R (Opcional)

```r
# No console R
install.packages(c("psych", "lavaan", "ggplot2", "dplyr", "tidyr"))
```

---

## 💻 Como Usar

### Execução Básica

#### 1. Aplicar o Questionário BFI-2

```bash
# Teste com contexto conversacional (recomendado)
python3 testeInContext.py output.csv

# Teste sem contexto
python3 testeNoContext.py output_nocontext.csv
```

**Saída:** CSV com colunas `id`, `statement`, `facet`, `reversed`, `response`

#### 2. Calcular Scores de Personalidade

```bash
python3 scores.py output.csv
```

**Saída no terminal:**
```
0  # Respostas inválidas
Scores de cada domínio:
BFI2_Extraversion: 3.25
BFI2_Agreeableness: 4.08
BFI2_Conscientiousness: 3.92
BFI2_Neuroticism: 2.33
BFI2_Openness: 4.17
```

#### 3. Análise de Múltiplos Testes

```bash
# Una múltiplos CSVs
python3 juntacsv.py

# Calcule scores combinados
python3 combined_scores.py
```

#### 4. Separe por Domínio

```bash
python3 separadominio.py
# Gera: Extraversion.csv, Agreeableness.csv, etc.
```

---

## 📊 Scripts Principais

### `testeInContext.py` ⭐

**Funcionamento:**
1. Verifica se o modelo customizado existe (cria se necessário)
2. Carrega os 60 itens do BFI-2
3. **Embaralha** os itens (evitar viés de ordem)
4. Apresenta cada item ao modelo
5. **Mantém histórico** de conversação
6. Salva respostas em CSV

**Prompt utilizado:**
```
Here are a number of characteristics that may or may not apply to you. 
Please indicate the extent to which you agree or disagree with the following statement. 
1 denotes 'strongly disagree', 2 denotes 'a little disagree', 3 denotes 'neither agree nor disagree', 
4 denotes 'little agree', 5 denotes 'strongly agree'. 
I am someone who: {item}
Answer:
```

### `scores.py`

**Cálculo de Scores:**
- Aplica inversão em itens marcados como `reversed: true`
- Calcula média por faceta (4 itens cada)
- Calcula média por domínio (3 facetas cada)
- Trata respostas inválidas substituindo por 3 (neutro)

**Fórmula de Inversão:**
```python
reversed_score = 6 - original_score
```

### `separadominio.py`

- Carrega `Psycho50.csv` e `bfi2facets.json`
- Aplica reversão onde necessário
- Cria 5 CSVs separados por domínio
- Facilita análises estatísticas específicas

---

## 📈 Análises Estatísticas

### Análises em Python

#### Estatísticas Descritivas
```bash
python3 stat.py invalid_responses.json
```

**Métricas calculadas:**
- Média de respostas inválidas
- Mediana
- Desvio padrão
- Quartis (Q1, Q3)

#### Distribuição Normal
```bash
python3 distNorm.py
```

#### Visualização Radar
```bash
python3 radar.py
```

### Análises em R

#### Análise Psicométrica Completa

```bash
Rscript ufsAnalysis.r
```

**Inclui:**
- **Alfa de Cronbach** (confiabilidade)
- **Análise Fatorial Confirmatória** (CFA)
- **Correlações entre domínios**
- **Análise de Componentes Principais** (PCA)

---

## 🎭 Experimentos com Personas

O diretório `WITH_PERSONA/` contém experimentos controlados com diferentes personas injetadas no prompt do sistema:

### Personas Testadas

| Persona | Descrição | Objetivo |
|---------|-----------|----------|
| `human/` | "Pretend you are a human" | Comportamento humano genérico |
| `man/` | Persona masculina | Investigar viés de gênero |
| `woman/` | Persona feminina | Investigar viés de gênero |
| `positive/` | Persona otimista | Testar viés de positividade |
| `humanNO/` | Sem instrução de simular humano | Baseline |

### Executar com Persona

```bash
cd WITH_PERSONA/human
python3 testeInContext.py output_human.csv
python3 scores.py output_human.csv
```

---

## 📊 Resultados

### Dataset Principal

- **`Psycho50.csv`**: 50 execuções completas do BFI-2
- **`Llama3Psycho50.csv`**: Versão específica Llama 3.1

### Arquivos de Análise

- **`matriz_correlacao.csv`**: Matriz de correlação entre itens
- **`FirstPCA.txt`**: Resultados da primeira análise PCA

### Estrutura dos Dados

**CSV de Respostas:**
```csv
id,statement,facet,reversed,response
1,"Is outgoing, sociable.",Sociability,False,4
16,"Tends to be quiet.",Sociability,True,2
... 
```

**CSV de Scores por Domínio:**
```csv
teste,BFI2_Extraversion,BFI2_Agreeableness,BFI2_Conscientiousness,BFI2_Neuroticism,BFI2_Openness
test1,3.25,4.08,3.92,2.33,4.17
test2,3.42,3.92,4.00,2.50,4.25
...
```

---

## 🔄 Pipeline Completo

```bash
# 1. Execute 50 testes
bash rodabfi.sh

# 2. Consolide respostas
python3 gather_responses.py

# 3. Calcule scores
python3 combined_scores.py

# 4. Separe por domínio
python3 separadominio.py

# 5. Análise estatística em R
Rscript ufsAnalysis.r

# 6. Visualize resultados
python3 radar.py
```

---

## 🛠️ Solução de Problemas

### Erro: "Model not found"

```bash
# Recrie o modelo customizado
ollama create llama3.1 -f Modelfile
```

### Respostas Inválidas

O script automaticamente:
- Conta respostas inválidas
- Substitui por 3 (neutro)
- Registra no output

### Ollama não conecta

```bash
# Verifique se o servidor está rodando
ollama list

# Reinicie o servidor
pkill ollama
ollama serve
```

---

Este projeto foi desenvolvido para fins de pesquisa acadêmica com apoio do **Programa de Bolsas Itaú (PBI)**.

---

## Agradecimentos

- **Itaú Unibanco S.A.** pelo apoio através do Programa de Bolsas Itaú (PBI)
- Comunidade **Ollama** pela infraestrutura de LLMs
- Desenvolvedores do **BFI-2** (Soto & John, 2017)

---

## Contato

Para dúvidas ou colaborações:
- GitHub: [@naomimori1](https://github.com/naomimori1)
- Issues: [Abra uma issue](https://github.com/naomimori1/icPsychometricsAI/issues)

---

## 🔗 Referências

- Soto, C. J., & John, O. P. (2017). The Big Five Inventory-2 (BFI-2). *Journal of Personality Assessment*, 99(1), 1-27.
- Ollama Documentation: https://ollama.com/
- BFI-2 Official: https://www.colby.edu/psych/personality-lab/
- Pellert, M., Lechner, C. M., Wagner, C., Rammstedt, B., & Strohmaier, M. (2024). AI Psychometrics: Assessing the Psychological Profiles of Large Language Models Through Psychometric Inventories. Perspectives on Psychological Science, 0(0). https://doi.org/10.1177/17456916231214460
-  Sühr, T, Dorner, F. E., Samadi, S., Kelava, A. : Challenging the Validity of Personality Tests for Large Language Models, arXiv preprint arXiv:2311.05297v2, 2024
- Mustafa Safdari, Greg Serapio-García, Clément Crepy, Stephen Fitz, Peter Romero, Luning
Sun, Marwa Abdulhai, Aleksandra Faust, and Maja Matari´c. Personality traits in large language
models. arXiv preprint arXiv:2307.00184, 2023
- Soto, C. J., & John, O. P. (2017). The next Big Five Inventory (BFI-2): Developing and assessing a hierarchical model with 15 facets to enhance bandwidth, fidelity, and predictive power. Journal of Personality and Social Psychology, 113, 117-143
- Zhang, Saizheng, Emily Dinan, Jack Urbanek, Arthur Szlam, Douwe Kiela and Jason Weston. “Personalizing Dialogue Agents: I have a dog, do you have pets too?” https://arxiv.org/abs/1801.07243
- Bodroža, Bojana, Bojana M. Dinić, and Ljubiša Bojić. "Personality testing of large language models: limited temporal stability, but highlighted prosociality." Royal Society Open Science 11, no. 10 (2024): 240180. https://doi.org/10.48550/arXiv.2306.04308
- Huang, J., Wang, W., Li, E.J., Lam, M.H., Ren, S., Yuan, Y., Jiao, W., Tu, Z., & Lyu, M.R. (2023). Who is ChatGPT? Benchmarking LLMs' Psychological Portrayal Using PsychoBench. ArXiv, abs/2310.01386.
- Dunn, T. J., Baguley, T., & Brunsden, V. (2014). From alpha to omega: a practical solution to the pervasive problem of internal consistency estimation. British journal of psychology (London, England : 1953), 105(3), 399–412. https://doi.org/10.1111/bjop.12046
- Revelle, William & Zinbarg, Richard. (2009). Coefficients Alpha, Beta, Omega, and the GLB: Comments on Sijtsma. Psychometrika. 74. 145-154. 10.1007/s11336-008-9102-z.
