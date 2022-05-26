import pandas as pd
import numpy as np
from unidecode import unidecode

def cria_modelo(filename, coluna, valor):
    table = pd.read_csv(filename)
    
    
    ## Frequency Table
    ## Sturges == k = 1 + (10/3).log n 
    n = table.shape[0]
    
    # Quantidade de classes
    k = int(round(1 + 3.322 * np.log10(n)))
    
    # Amplitude de cada classe
    c = n/k # -> só pra nois printar bonitinho dps

    print(n)
    print(k)
    print(c)
    gasolina_comum = table[table[coluna].str.match(valor)]
    print(len(gasolina_comum))

    #gasolina_comum = table[table['COMBUSTÍVEL'].str.match(comb1)]
    frequency = pd.value_counts(
    pd.cut(x = gasolina_comum['PREÇO VENDA'], bins = k, include_lowest = True))
# Deu key error no 'range'
    
    percentage = pd.value_counts(
    pd.cut(x=gasolina_comum['PREÇO VENDA'], bins = k, include_lowest = True), normalize = True) * 100

    ## Formatting Frequency Table
    frequency_table = ({'Frequência' : frequency, 'Porcentagem' : percentage})

    ## Transforming into DataFrame
    frequency_table = pd.DataFrame(frequency_table)
    #frequency_table = pd.DataFrame(frequency_table, index=[i for i in range(1, frequency.shape[0] + 1)])
    freq_table_final = frequency_table.copy(deep=False)

# 
#meu deus
    #freq_table_final.sort_values('Range')
    ## Reseting index
    frequency_table.reset_index(inplace=True)
    
    ## Renaming columns
    freq_table_final.rename(columns={'index' : 'Range'}, inplace = True)

    #freq_table_final = freq_table_final.iloc[freq_table_final['Index'].cat.codes.argsort()]

    #freq_table_final.insert(1, 'Contagem')
    freq_table_final['Contagem'] = frequency_table['Frequência'].copy()

    for i, row in freq_table_final.iterrows():
        ifor_val = '|'* freq_table_final['Frequência'][i]
        freq_table_final.loc[i,'Contagem'] = ifor_val

    #cols = freq_table_final.columns.tolist()
    #cols = [cols[0], cols[3], cols[1], cols[2]]
    #print(type(cols))
    #freq_table_final = freq_table_final[cols]
    
    coluna = unidecode(coluna).lower().replace(' ','_')
    valor = unidecode(valor).lower().replace(' ','_')

    freq_table_final.to_csv(f'./resultados_csv/modelo_resultado_{coluna}_{valor}.csv')        

    ## Columns types
    print(freq_table_final)

cria_modelo('./resultados_csv/resultado_diesel.csv', 'BANDEIRA', 'NACIONAL')
#cria_modelo('./resultados_csv/resultado_diesel_s10.csv', 'COMBUSTÍVEL','DIESEL S10')
