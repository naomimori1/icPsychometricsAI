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
