import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#https://matplotlib.org/stable/plot_types/stats/boxplot_plot.html

def exploracao(filename):
    dataframe = pd.read_csv(filename)
    dataframe.boxplot(column=['PREÇO VENDA'])

'''
Pra achar os quantis:
Q1 = dataframe.quantile(0.25)
Q2 = dataframe.quantile(0.5) --> também a mediana
Q3 = dataframe.quantile(0.75)
Pra detectar os outliers extremos, o ideal seria rodar o boxplot
e identificar onde tem os extremos, e depois rodar uma linha pedindo
pra imprimir as linhas que possuem valores próximos aos que a gente identificou
no olho que são os outliers
Link de uma imagem exemplificando: https://miro.medium.com/max/1400/1*2c21SkzJMf3frPXPAR_gZA.png
Pra calcular o IQR:
IQR = Q3-Q1

'''
exploracao('./resultados_csv/resultado_diesel_s10.csv')

