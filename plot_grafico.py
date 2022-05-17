import pandas as pd
import matplotlib as mp
import seaborn as sns

def plot_grafico(filename):
    frequency_table = pd.read_csv(filename)

    ax = sns.countplot(x="Frequência",data=frequency_table)
    

plot_grafico('modelo_resultado_diesel.csv')