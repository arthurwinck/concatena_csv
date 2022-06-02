import pandas as pd
import numpy as np
from unidecode import unidecode

def filtra_por_coluna(filename, coluna, valor, comb):
    df = pd.read_csv(filename)

    df = df[df[coluna] == valor]
    #df = df.query(f"{coluna} == {valor}")
    coluna = coluna.lower()
    valor = valor.lower()
    df.to_csv(f'./resultados_csv/resultado_{unidecode(comb).lower()}_{unidecode(coluna).lower()}_{unidecode(valor).lower()}_novo.csv')

filtra_por_coluna('./resultados_csv/resultado_diesel.csv', 'BANDEIRA', 'NACIONAL', 'diesel')
filtra_por_coluna('./resultados_csv/resultado_diesel.csv', 'BANDEIRA', 'OUTRO', 'diesel')

filtra_por_coluna('./resultados_csv/resultado_diesel_s10.csv', 'BANDEIRA', 'NACIONAL', 'diesel_s10')
filtra_por_coluna('./resultados_csv/resultado_diesel_s10.csv', 'BANDEIRA', 'OUTRO', 'diesel_s10')

filtra_por_coluna('./resultados_csv/resultado_diesel.csv', 'REGIÃO', 'METRÓPOLE', 'diesel')
filtra_por_coluna('./resultados_csv/resultado_diesel.csv', 'REGIÃO', 'INTERIOR', 'diesel')

filtra_por_coluna('./resultados_csv/resultado_diesel_s10.csv', 'REGIÃO', 'METRÓPOLE', 'diesel_s10')
filtra_por_coluna('./resultados_csv/resultado_diesel_s10.csv', 'REGIÃO', 'INTERIOR', 'diesel_s10')