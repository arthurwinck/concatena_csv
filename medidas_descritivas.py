import pandas as pd
import numpy as np

def populate_ponto_medio(filename):
    file = open(filename)
    lista_pm = []
    lista_freq = []

    for i, line in enumerate(file.readlines()):
        if i == 0:
            continue


        lista_colunas = line.split(',')

        freq = lista_colunas[2]
        
        try:
            freq = int(freq)
        except Exception as e:
            raise e
        
        lista_freq.append(freq)

        classe = [lista_colunas[0].replace('"','').replace('(',''),lista_colunas[1].replace('"','').replace(']','')]
        print(classe)

        try:
            menor = float(classe[0])
            maior = float(classe[1])
            soma = (maior-menor)/2
            pm = menor+soma
            lista_pm.append(np.round(pm, decimals=3))
        except Exception as e:
            raise e


    total = sum(lista_freq)

    print(lista_pm)
    print(lista_freq)

    #Cria o dataframe, deve ser mais fácil calcular a partir disso
    table_freq_pm = pd.DataFrame(list(zip(lista_freq,lista_pm)))

    
    #Média
    media_pond = sum(map(lambda x, y: x*y, lista_freq, lista_pm))/total
    print(f"MÉDIA: {sum(map(lambda x, y: x*y, lista_freq, lista_pm))/total}")
    #Moda
    print(f"MODA: {lista_pm[lista_freq.index(max(lista_freq))]}")
    #Mediana
    print(f"MEDIANA: {table_freq_pm[0].median()}")
    
    # half = total/2
    # lista_half = []
    # if half % 2 == 0:
    #     lista_half.append(half)
    #     lista_half.append(half+1)
    # else:
    #     lista_half.append((half-1)/2+1)
    
    # sum_half = 0
    # for i, freq in enumerate(lista_freq):
    #     if len(lista_half) > 1:
    #         sum_half += freq
            
    #         if sum_half > 

    # lista_pontos_medios = [pm1, pm2, pm3]
    # lista_freq -> [1, 2, 5] = 

    half = total/2 # --> total = 6, half = 3,4

    for i, freq in enumerate(lista_freq):
        half -= freq

        if half <= 0:
            if (total/2) // 2 == 0:
                if half == 0:
                    print(f"MEDIANA: {(lista_pm[i]+lista_pm[i+1])/2}") 
                    break
                else:
                    print(f"MEDIANA: {lista_pm[i]}")
                    break 
            else:
                print(f"MEDIANA: {lista_pm[i]}")
                break 

    # def std(list):
    #avg = sum(list)/float(len(list))
    #return math.sqrt(sum(map(lambda x: (x-avg)**2,list))/len(list))

    variancia = 0

    for i, num in enumerate(lista_freq):
        variancia += num*(lista_pm[i] - media_pond)**2

    print(f"VARIÂNCIA: {variancia/total}")
    desv = np.sqrt(variancia/total)
    print(f"DESVIÃO PADRÃO: {desv}")

    # Obtenha, do(s) modelo(s) empírico(s), as principais estatísticas descritivas (valor central:
    #  a média, a mediana e a moda (se existir); dispersão: variância, desvio padrão, erro padrão da média
    #  e coeficiente de variação; forma: assimetria) para analisar as situações desejadas. 

    #Altera aqui gugu o path pro modelo que tu quer exportar
    table_freq_pm.to_csv('./resultados_csv/tabela_pm_freq.csv')

#Altera aqui gugu o path pro modelo que tu quer importar
populate_ponto_medio('./csvs_montados/media_diesel_s10.csv')
