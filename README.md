# Departamento de Informática - Universidade Federal de Viçosa
## Visualização de Dados 2022/01 - INF 723
## Profa. Sabrina de Azevedo Silveira

## Trabalho Prático
**Desenvolver um projeto relacionado ao seu trabalho de pós-graduação. Este projeto deve realizar uma proposta de representação visual interativa aplicada ao trabalho de mestrado/doutorado.**


[TOC]


## Base de Dados
- 4 meses de logs de autorizações da rede sem fio
- 14,2m requisições
- dispositivos (36k dispositivos) - sem localização exata
- ponto de acesso (108 aps)
- timestamp
- método de autenticação utilizado (dado extremamente incompleto)

## Caracterização Anterior
A caracterização anterior, em visualização clássica e sem interatividade.

![Caracterização Anteriror](docs/caracterizacao_antrerior.jpg)

## Base de Dados Reprocessada

Base de dados processada com dados estatísticos simples, porém para
otimizar a inicialização dos datasets.

Novas bases:
- df_client
- df_ap

## Objetivos da Visualização
Apresentar o dataset de forma interativa para atrair maiores usuários interessados. Áreas de interesses:
- redes
- gestão de identidades
- mobilidade

Mostrar as características do dataset com informação sobre demanda, análise de um grupo específico de dados, ajustes dinâmicos, ampliação e redução da visualização, seleção com sliders e menus flutuantes.

**Contribuição Principal:**
Dataset será disponibilizado para a comunidade acadêmica, e a apresentação da base de dados de forma interativa poderá trazer maiores interessados.

## Ferramentas
Python 3.9.2
- Plotly 5.8.0
- Dash 2.4.1 / Flask 2.1.2
- NumPy 1.22.4
- Pandas 1.4.2


## Opções da Visualização
- Características da base de dados
- Escolha de Dispositivo para Comparação
- Seleção de Grupos (visível / ocultado)
- Seleção para Top Pontos de Acessos

![Caracterização Anteriror](docs/caracterizacao_atual.jpg)

## Contatos:
Airton Ribeiro Filho

airton.r.filho@ufv.br
