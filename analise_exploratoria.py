import pandas as pd
import numpy as np


def analise_exploratoria(filename):
    dataframe = pd.read_csv(filename)

    q1 = dataframe.quantile(0.25)
    q2 = dataframe.quantile(0.5) #--> também a mediana
    q3 = dataframe.quantile(0.75)

    print('PRIMEIRO QUARTIL ------------------------------')
    print(q1)
    print('SEGUNDO QUARTIL ------------------------------')
    print(q2)
    print('TERCEIRO QUARTIL ------------------------------')
    print(q3)

    icr = q3-q1
    #minimum = (q1 - 1.5*icr) # Menor que esse valor, é outlier (no exemplo que eu testei eu não achei, deu baixo)
    #maximum = (q3 + 1.5*icr) # Maior que esse valor, é outlier (esses aí eu achei kkkkkk tá osso ser brasileiro)
    #outlier_sup = dataframe['PREÇO VENDA'].max()
    #outlier_inf = dataframe['PREÇO VENDA'].min()

    #Limites do outlier inferior
    lim_min_inf = q1 - 3*icr
    lim_max_inf = q1 - 1.5*icr


    #Limites do outlier superior
    lim_min_sup = q3 + 1.5*icr
    lim_max_sup = q3 + 3*icr

    #Limites de outliers extremos
    lim_extremo_inf = q1 - 3*icr
    lim_extremo_sup = q3 + 3*icr 


    #dataframe[(dataframe['PREÇO VENDA'] < lim_extremo_inf) | (dataframe['PREÇO VENDA'] > lim_extremo_inf)]

    #outliers_inf = dataframe[(dataframe['PREÇO VENDA'] > lim_min_inf) & (dataframe['PREÇO VENDA'] < lim_max_inf)]
    #outliers_sup = dataframe[(dataframe['PREÇO VENDA'] > lim_min_sup) & (dataframe['PREÇO VENDA'] < lim_max_sup)]

    #outliers_ext_inf = dataframe[(dataframe['PREÇO VENDA'] < lim_extremo_inf)]
    #outliers_ext_sup = dataframe[(dataframe['PREÇO VENDA'] > lim_extremo_sup)]

    
    #dataframe[(dataframe['PREÇO VENDA'] > lim_min_inf) & (dataframe['PREÇO VENDA'] < lim_max_inf)]
    #outliers_superior = dataframe[((dataframe < (lim_max_sup)) | (dataframe > (lim_min_sup)))]
    
    

    #outliers_sup = dataframe.loc[(dataframe['PREÇO VENDA'] <= lim_max_sup) & (dataframe['PREÇO VENDA'] >= lim_min_sup)] 
    #outliers_sup = dataframe.query(f"{lim_min_sup} <= 'PREÇO VENDA' <= {lim_max_sup}")
    #outliers_sup = dataframe['PREÇO VENDA']
    
    dataframe = pd.DataFrame(dataframe['PREÇO VENDA'])

    outliers_sup = dataframe[((dataframe <= (lim_max_sup)) & (dataframe >= (lim_min_sup)))]
    outliers_inf = dataframe[((dataframe <= (lim_max_inf)) & (dataframe >= (lim_min_inf)))]
    outliers_ext_sup = dataframe[(dataframe > (lim_extremo_sup))]
    outliers_ext_inf = dataframe[(dataframe < (lim_extremo_inf))]

    print("------------------------------------------------")
    print(f"OUTLIER SUPERIOR: Limite Máximo:")
    print(lim_max_sup)
    print("Limite Mínimo:")
    print(lim_min_sup)
    print(outliers_sup.dropna())

    print("------------------------------------------------")
    print(f"OUTLIER INFERIOR: Limite Máximo:")
    print(lim_max_inf)
    print("Limite Mínimo:")
    print(lim_min_inf)
    print(outliers_inf.dropna())

    print("------------------------------------------------")
    print(f"OUTLIER EXTREMO SUPERIOR: Limite:")
    print(lim_extremo_sup)
    print(outliers_ext_sup.dropna())
    
    print("------------------------------------------------")
    print(f"OUTLIER EXTREMO INFERIOR: Limite:")
    print(lim_extremo_inf)
    print(outliers_ext_inf.dropna())


analise_exploratoria('./resultados_csv/resultado_diesel_regiao_metropole_novo.csv')