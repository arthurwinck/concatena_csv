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

    #Cria o dataframe, deve ser mais fácil calcular a partir disso
    table_freq_pm = pd.DataFrame(list(zip(lista_freq,lista_pm)))

    print(lista_freq)
    print(lista_pm)

    print('\n------------- MEDIDAS AGRUPADAS ------------------')
    #Média
    media_pond = sum(map(lambda x, y: x*y, lista_freq, lista_pm))/total
    print(f"MÉDIA: {media_pond}")
    
    #Moda -- Checar se a moda é única
    moda = lista_pm[lista_freq.index(max(lista_freq))]
    print(f"MODA: {moda}")
    
    #Mediana -- Alterar para cálculo em relação ao gráfico
    half = total/2 # --> total = 6, half = 3,4
    mediana = 0

    for i, freq in enumerate(lista_freq):
        half -= freq

        if half <= 0:
            if (total/2) // 2 == 0:
                if half == 0:
                    classe_mediana = i
                    print(f"MEDIANA: {(lista_pm[i]+lista_pm[i+1])/2}") 
                    break
                else:
                    classe_mediana = i                   
                    print(f"MEDIANA: {lista_pm[i]}")
                    break 
            else:
                classe_mediana = i
                print(f"MEDIANA: {lista_pm[i]}")
                break 


    ind = classe_mediana
    inferior = lista_pm[ind] - (maior-menor)/2
    print(inferior)
    

    variancia = 0
    for i, num in enumerate(lista_freq):
        variancia += num*(lista_pm[i] - media_pond)**2

    print(f"VARIÂNCIA: {variancia/total}")
    desv = np.sqrt(variancia/total)
    print(f"DESVIÃO PADRÃO: {desv}")

    cv = desv/media_pond
    print(f"CV: {cv}")

    #Assimetria tem que pegar a moda, não sei se tá correto por causa do cálculo da moda
    assimetria = (media_pond - moda)/desv
    print(f'ASSIMETRIA: {assimetria}')

    #Isso aqui tá zoado 100%
    #Mediana não é "ajustada" pode ser por isso que tá zoado
    assimetria2 = (3*media_pond - 2*mediana)/desv
    print(f'ASSIMETRIA S/MODA: {assimetria2}')

    print('\n-------------------------------')

    # Obtenha, do(s) modelo(s) empírico(s), as principais estatísticas descritivas (valor central:
    #  a média, a mediana e a moda (se existir); dispersão: variância, desvio padrão, erro padrão da média
    #  e coeficiente de variação; forma: assimetria) para analisar as situações desejadas. 

    #Altera aqui gugu o path pro modelo que tu quer exportar
    table_freq_pm.to_csv('./resultados_csv/tabela_pm_freq.csv')

#Altera aqui gugu o path pro modelo que tu quer importar
populate_ponto_medio('./csvs_montados/media_diesel_s10.csv')

table = pd.read_csv('./resultados_csv/resultado_diesel_s10.csv')

print('\n------------- MEDIDAS NÃO-AGRUPADAS ------------------')
print(f"mediana: {table['PREÇO VENDA'].median()}")
print(f"moda: {table['PREÇO VENDA'].mode()}")
print(f"cv: {table['PREÇO VENDA'].std()/table['PREÇO VENDA'].mean()}")
print(table['PREÇO VENDA'].describe())
print('-------------------------------\n')
