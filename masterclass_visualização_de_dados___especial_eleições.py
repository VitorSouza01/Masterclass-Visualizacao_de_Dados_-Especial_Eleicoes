# -*- coding: utf-8 -*-
"""Masterclass - Visualização de Dados _ Especial Eleições.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EY96csXv-rA2WZZHVitDyaCF5Kmgen_W
"""

# Macro
# Prefeitos / Vereadores
# Analise de Comportamento

# Modelagem de dados
import pandas as pd
import numpy as np

# Graficas
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Avisos
import warnings
warnings.filterwarnings('ignore')

# Configurações no pandas
pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', 100)

# Configurações no Matplot
plt.rcParams['figure.figsize'] = (15, 6)
plt.style.use('ggplot')

"""# **Importação dos dados**"""

# Dados
Base_Dados = pd.read_csv('clean_data.csv')

# Dimensao
Base_Dados.shape

# Verificar
Base_Dados.head()

# Info
Base_Dados.info()

# Nulos
Base_Dados.isnull().sum()

# Campos unicos
Base_Dados.nunique()

# Retirar a coluna
Base_Dados.drop(columns=['Unnamed: 0'], inplace=True)

# Verificar
Base_Dados.head()

"""# **Analise Macros**

## **Prefeitos eleitos no país**
"""

# Campos unicos
Base_Dados['job'].unique(), Base_Dados['elector_count'].unique()

# Filtro
Query_Prefeitos = Base_Dados[
    (Base_Dados['job'] == 'prefeito') &
    (Base_Dados['elector_count'] == 's')
]

# Dimensão
Query_Prefeitos.shape

# Analise
Analise_01 = Query_Prefeitos.groupby(by=['main_party']).agg(
    Quantidade=('candidate_vote_count', 'count')
)

# Verificar
Analise_01.head()

# Quantidade Prefeitos Eleitos
Qtd_Prefeitos_Eleitos = Analise_01['Quantidade'].sum()

Qtd_Prefeitos_Eleitos

# Gerando Porcentual
Analise_01['%'] = Analise_01['Quantidade'] / Qtd_Prefeitos_Eleitos * 100
Analise_01['%'] = round(Analise_01['%'], 2)

# Ordenar
Analise_01.sort_values('Quantidade', inplace=True, ascending=False)

# Vertical
Analise_01.head()

# Paletas de cores
sns.color_palette('magma', len(Analise_01))

# Tamanho
plt.figure(figsize=(20, 6))

# Paleta
Paleta_Cores = sns.color_palette('magma', len(Analise_01))

#Plot
plt.bar(
    Analise_01.index,
    Analise_01['Quantidade'],
    width=0.9,
    color=Paleta_Cores
    )

# Titulo
plt.title('Prefeitos eleitos no país', loc='left', fontsize=20, color='#404040', fontweight=600)

# Labels
plt.ylabel('Quantidade de prefeitos')
plt.xlabel('Partidos')
plt.xticks(rotation=90)

# Ajustando escala do gráfico
plt.ylim(0, Analise_01['Quantidade'].max() + (Analise_01['Quantidade'].max() * 0.1))

# Incluindo os dados no gráfico
for Posicao, Valor in enumerate(Analise_01['Quantidade']):
    plt.text(
        # Posição do gráfico (x, y)
        Posicao - 0.3, Valor + 10,
        # Valor no gráfico
        Valor,
        # Paleta
        color=Paleta_Cores[Posicao],
        # Tamanho
        size=12,
        # Espessura da fonte
        fontweight=700
    )

# Total de eleitos
Total_Eleitos = Analise_01['Quantidade'].sum()

# Info complementar
plt.annotate(
    f'Eleitos Brasil: {Total_Eleitos}',
    xy=(0.99, 0.94),
    xycoords='axes fraction',
    ha='right',
    va='center',
    color='green',
    fontsize=14,
    fontweight=500,
    bbox=dict(facecolor='#ffffff', edgecolor='green', boxstyle='round', pad=0.25),
);

"""## **Vereadores eleitos no país**"""

# Filtro
Query_Vereadores = Base_Dados[
    (Base_Dados['job'] == 'vereador') &
    (Base_Dados['elector_count'] == 's')
]

# Dimensão
Query_Vereadores.shape

# Analise
Analise_02 = Query_Vereadores.groupby(by=['main_party']).agg(
    Quantidade=('candidate_vote_count', 'count')
)

# Verificar
Analise_02.head()

# Quantidade Vereadores Eleitos
Qtd_Vereadores_Eleitos = Analise_02['Quantidade'].sum()

Qtd_Vereadores_Eleitos

# Gerando Porcentual
Analise_02['%'] = Analise_02['Quantidade'] / Qtd_Vereadores_Eleitos * 100
Analise_02['%'] = round(Analise_02['%'], 2)

# Ordenar
Analise_02.sort_values('Quantidade', inplace=True, ascending=False)

# Vertical
Analise_02.head()

# Tamanho
plt.figure(figsize=(12, 10))

# Plot das linhas
plt.hlines(
    # Dados
    y = Analise_02.index,
    xmin = 0,
    xmax = Analise_02['Quantidade'],
    # Espessura da linha
    lw = 5,
    # Paleta
    color = Paleta_Cores,
    # Transparencia
    alpha = 0.5
)

# Plot das pontos
plt.scatter(
    # Dados
    Analise_02['Quantidade'],
    Analise_02.index,
    # Tamanho do ponto
    s = 100,
    # Cor
    color = Paleta_Cores,
    # Transparencia
    alpha = 0.8
)

# Titulo
plt.title('Vereadores eleitos no país', loc='left', fontsize=20, color='#404040', fontweight=500);

# Total de eleitos
Total_Eleitos = Analise_02['Quantidade'].sum()

# Info complementar
plt.annotate(
    f'Eleitos Brasil: {Total_Eleitos}',
    xy=(0.99, 0.94),
    xycoords='axes fraction',
    ha='right',
    va='center',
    color='green',
    fontsize=14,
    fontweight=500,
    bbox=dict(facecolor='#ffffff', edgecolor='green', boxstyle='round', pad=0.25),
);

"""## **Analise de Correlação**"""

len(Analise_01), len(Analise_02)

# Tab
Tab_Correlacao = Analise_01['Quantidade'].reset_index()

# Cruzamento
Tab_Correlacao = pd.merge(Tab_Correlacao, Analise_02.reset_index(), on=['main_party'], how='inner')

# Ajustar
Tab_Correlacao.columns = ['Partido', 'Prefeitos', 'Vereadores', '%']

# Drop
Tab_Correlacao.drop(columns = ['%'], inplace=True)

# Verificando
Tab_Correlacao.head()

# Plot de regressão

sns.regplot(
    # Dados
    x = Tab_Correlacao['Prefeitos'],
    y = Tab_Correlacao['Vereadores'],

    # Intervalo de confiança para estimar a regressão
    ci = 95,

    # Cor dos pontos
    scatter_kws={
        'color' : 'blue',
        's' : 80,
        'alpha' : 0.5
    },

    # Cor da linha
    line_kws={
        'color' : 'red',
        'alpha' : 0.2,
        'lw' : 2
    },
)

# Titulo
plt.title('Prefeiros x Vereadores eleitos')

# Loop para incluir os textos
for Linha in range(0, Tab_Correlacao.shape[0]):

    # Incluindo os valores
    plt.text(
        Tab_Correlacao['Prefeitos'][Linha] + 0.8,
        Tab_Correlacao['Vereadores'][Linha],
        Tab_Correlacao['Partido'][Linha],
        size = 'medium',
        color = 'gray',
        weight = 'semibold'
    )

"""## **Plot Tridimensional**"""

# Sumarizando quantidade de candidatos
Quantidade_Candidatos = Base_Dados.groupby(by=['main_party']).count().iloc[:,0:1].reset_index()

# Renomear colunas
Quantidade_Candidatos.columns = ['Partido', 'Candidatos']

# Verificar
Quantidade_Candidatos.head()

Tab_Correlacao.head()

# Cruzar
Tab_Correlacao = pd.merge(Tab_Correlacao, Quantidade_Candidatos, on=['Partido'], how='inner')

# Verificando
Tab_Correlacao.head()

# Correlação
Tab_Correlacao.corr()

# 1 a -1
# proxima 1: positiva (ambos crescem)
# proxima -1: negativa (um cresce, outro desce)

# Plot Tridimensional

# Tamanho
Figura = plt.figure(figsize = (15, 8))

# Instanciar
Eixo = Figura.add_subplot(111, projection='3d')

# Plot
Eixo.scatter(
    Tab_Correlacao['Prefeitos'],
    Tab_Correlacao['Vereadores'],
    Tab_Correlacao['Candidatos'],
    c = 'black',
    s = 100
)

# Rotação
Eixo.view_init(30, 185)

# Labels
Eixo.set_xlabel('Prefeitos')
Eixo.set_ylabel('Vereadores')
Eixo.set_zlabel('Candidatos')

Figura = px.scatter_3d(
    Tab_Correlacao,
    x = 'Prefeitos',
    y = 'Vereadores',
    z = 'Candidatos',
    color = 'Partido',
    opacity = 0.7,
    symbol = 'Partido'
)

Figura.show()