# Interpretador miniPar

Projeto desenvolvido para a disciplina de Compiladores 2024.2.  
Grupo: Antônio, Bruno, Eneas, Herberty e Leonardo

## Descrição

Este repositório contém um interpretador simples para a linguagem miniPar. O objetivo é implementar um analisador léxico, sintático e semântico, além de executar instruções e manipular mensagens de interface gráfica.

## Funcionalidades

- **lexer.py**: Identifica os tokens da linguagem.
- **parser.py**: Realiza a análise de estrutura da linguagem.
- **semantic.py**: Verifica a validade semântica do código.
- **exec.py**: Processa as instruções do código em tempo de execução.

## Requisitos

- Python 3.13
- Bibliotca PLY (pip install ply)

## Como Usar

1. Clone o repositório:

   ```bash
   git clone https://github.com/AnriaW/interpretador-miniPar.git
   ```
2. Abra o terminal, navegue até a pasta do projeto e digite o seguinte comando para executar o programa:
```sh
python main.py <nome_do_programa.mp>
```
***Exemplo:***
```sh
python3 main.py teste2.mp
```

