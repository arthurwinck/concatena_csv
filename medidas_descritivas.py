import pandas as pd
import numpy as np
import glob
from unidecode import unidecode

def populate_ponto_medio(nome, tabela_modelo, tabela_simples, coluna, valor):
    file = open(tabela_modelo)
    lista_pm = []
    lista_freq = []
    lista_intervalos = []

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
        #print(classe)

        try:
            menor = float(classe[0])
            maior = float(classe[1])
            soma = (maior-menor)/2
            pm = menor+soma
            lista_pm.append(np.round(pm, decimals=3))
            lista_intervalos.append((menor,maior))
        except Exception as e:
            raise e


    total = sum(lista_freq)

    #Cria o dataframe, deve ser mais fácil calcular a partir disso
    table_freq_pm = pd.DataFrame(list(zip(lista_freq,lista_pm)))

    #print(lista_freq)
    #print(lista_pm)

    #print('\n------------- MEDIDAS AGRUPADAS ------------------')
    #Média
    media_pond = sum(map(lambda x, y: x*y, lista_freq, lista_pm))/total
    #print(f"MÉDIA: {media_pond}")
    
    #Moda -- Checar se a moda é única
    ind_moda = lista_freq.index(max(lista_freq))
    l = lista_intervalos[ind_moda][0]

    if ind_moda < len(lista_freq) - 1:
        moda = l + (lista_freq[ind_moda] - lista_freq[ind_moda-1])/(2*lista_freq[ind_moda] - lista_freq[ind_moda-1] - lista_freq[ind_moda+1])*(lista_intervalos[ind_moda][1] - lista_intervalos[ind_moda][0])
    else:
        moda = l + (lista_freq[ind_moda] - lista_freq[ind_moda-1])/(2*lista_freq[ind_moda] - lista_freq[ind_moda-1] - lista_freq[ind_moda])*(lista_intervalos[ind_moda][1] - lista_intervalos[ind_moda][0])
    #print(f"MODA: {moda}")
    
    #Mediana -- Alterar para cálculo em relação ao gráfico
    half = total/2 # --> total = 6, half = 3,4
    mediana = 0

    for i, freq in enumerate(lista_freq):
        half -= freq

        if half <= 0:
            if (total/2) // 2 == 0:
                if half == 0:
                    classe_mediana = i
                    break
                else:
                    classe_mediana = i
                    break 
            else:
                classe_mediana = i
                break 


    #P(X<=~X) = 0,5
    # Usar a frequência acumulada -> vai somando desde a primeira classe até 100%
    #6.63 -> 6.84 (classe que possui os 50%) possui 18,73
    #Anterior a essa classe
    
    #Cálculo da mediana
    #int_maior, int_menor e a freq vem da classe que possui os 50%
    #(int_maior - int_menor) / freq da classe (%) = (~x - int_menor)/50% - freq_acumulada (%)
    lista_freq_por = list(map(lambda x: x/total, lista_freq))
    
    lista_freq_ac = [0]*len(lista_freq_por)
    for i, freq in enumerate(lista_freq_por):
        lista_freq_ac[i] = sum(lista_freq_por[:i]) + lista_freq_por[i]

    
    ind = classe_mediana
    dif = (maior-menor)/2
    inferior = lista_intervalos[ind][0] 
    superior = lista_intervalos[ind][1]
    #print(f"inferior: {inferior} superior: {superior}")

    mediana = (0.5 - lista_freq_ac[ind-1])*(superior - inferior)/lista_freq_por[ind] + inferior 
    #print(f"MEDIANA: {mediana}")

    # variancia = 0
    # for i, num in enumerate(lista_freq):
    #     variancia += num*(lista_pm[i] - media_pond)**2

    variancia = sum(map(lambda x, y: x*(y - media_pond)**2, lista_freq, lista_pm))/total
    media_pond = sum(map(lambda x, y: x*y, lista_freq, lista_pm))/total


    #print(f"VARIÂNCIA: {variancia/total}")
    #print(f"VARIÂNCIA: {variancia_teste/total}")

    desv = np.sqrt(variancia)
    #print(f"DESVIÃO PADRÃO: {desv}")

    cv = desv/media_pond
    #print(f"CV: {cv}")

    #Assimetria tem que pegar a moda, não sei se tá correto por causa do cálculo da moda
    assimetria = (media_pond - moda)/desv
    #print(f'ASSIMETRIA: {assimetria}')

    #Isso aqui tá zoado 100%
    #Mediana não é "ajustada" pode ser por isso que tá zoado
    assimetria2 = 3*(media_pond - mediana)/desv
    #print(f'ASSIMETRIA S/MODA: {assimetria2}')

    #print('\n-------------------------------')

    # Obtenha, do(s) modelo(s) empírico(s), as principais estatísticas descritivas (valor central:
    #  a média, a mediana e a moda (se existir); dispersão: variância, desvio padrão, erro padrão da média
    #  e coeficiente de variação; forma: assimetria) para analisar as situações desejadas. 

    # #Altera aqui gugu o path pro modelo que tu quer exportar!!!!
    # table_freq_pm.to_csv('./resultados_csv/tabela_pm_freq.csv')

    table = pd.read_csv(tabela_simples)

    if coluna != None and valor != None: 
        table = table[table[coluna]==valor]

    print(table)

    # print('\n------------- MEDIDAS NÃO-AGRUPADAS ------------------')
    # print(f"mediana: {table['PREÇO VENDA'].median()}")
    # print(f"moda: {table['PREÇO VENDA'].mode()}")
    # print(f"cv: {table['PREÇO VENDA'].std()/table['PREÇO VENDA'].mean()}")
    # print(table['PREÇO VENDA'].describe())
    # print('-------------------------------\n')


    tp = table['PREÇO VENDA']

    data = {'Medidas': ['MÉDIA (R$)', 'MODA (R$)', 'MEDIANA (R$)', 'VARIÂNCIA (R$)^2', 'DESVIO (R$)', 'CV (ADIM)', 'ASSIMETRIA (ADIM)', 'ASSIMETRIA S/MODA (ADIM)'],
            'Dados Agrupados': [media_pond, moda, mediana, variancia, desv, cv, assimetria, assimetria2],
            'Dados Não-Agrupados': [tp.mean(), tp.mode()[0], tp.median(), tp.var(), tp.std(), tp.std()/tp.mean(), (tp.mean()-tp.mode()[0])/tp.std(), (tp.mean()-tp.mode()[0])/tp.std()]
            }

    
    column_erro = []
    for i, item in enumerate(data['Dados Agrupados']):
        column_erro.append(np.round(100*(abs(data['Dados Não-Agrupados'][i] - item))/data['Dados Não-Agrupados'][i], 3))
        data['Dados Agrupados'][i] = np.round(data['Dados Agrupados'][i], 3)
        data['Dados Não-Agrupados'][i] = np.round(data['Dados Não-Agrupados'][i], 3)


    data['Erro Relativo'] = column_erro

    table_result = pd.DataFrame(data)
    


    print(table_result)
    #(media_pond - moda)/desv
    print(f"Agrupado: {assimetria} = ({media_pond} - {moda})/{desv}")
    print(f"Não-agrupado: {(tp.mean()-tp.mode()[0])/tp.std()} = ({tp.mean()}-{tp.mode()[0]})/{tp.std()}")
    


    # !!!!! - Caso queria exportar para csv

    if coluna != None and valor != None:
        table_result.to_csv(f"./medidas_descritivas/medidas_descritivas_{unidecode(coluna.replace(' ','_').lower())}_{unidecode(valor.replace(' ','_').lower())}.csv")
    else:
        table_result.to_csv(f"./medidas_descritivas/medidas_descritivas_{nome}.csv")

    #Criação da tabela de variáveis
    k = len(lista_intervalos)
    amplitude_total = table['PREÇO VENDA'].max() - table['PREÇO VENDA'].min()
    c = abs(lista_intervalos[0][1] - lista_intervalos[0][0])
    print(f"R: {amplitude_total} / K: {k} / C: {c}")

    name = ''

    for i in range(len(nome.split('_'))):
        name += nome.split('_')[i].capitalize() + ' '        

    name = name[:-1]

    #name = nome.split('_')[0].capitalize() + ' ' + nome.split('_')[1].capitalize()

    return {'k': k, 'r': amplitude_total, 'c': c, 'name': name}

# tabela_modelo -> tabela do modelo empírico criado a partir dos dados simples
# tabela_simples -> tabela de dados não agrupados para usar como referência
# tabela_export -> tabela que será exportada com as medidas descritivas e os erros
# populate_ponto_medio(tabela_modelo, tabela_simples, tabela_export)
#populate_ponto_medio('diesel', './resultados_csv/modelo_resultado_combustivel_diesel.csv', './resultados_csv/resultado_diesel.csv', None, None)
#populate_ponto_medio('diesel_s10', './resultados_csv/modelo_resultado_bandeira_nacional.csv', './resultados_csv/resultado_diesel_bandeira_nacional.csv', 'BANDEIRA', 'NACIONAL')
populate_ponto_medio('diesel_nacional', './resultados_csv/modelo_resultado_diesel_bandeira_nacional.csv', './resultados_csv/resultado_diesel_bandeira_nacional.csv', 'BANDEIRA', 'NACIONAL')


def cria_tabela_var():
    lista_dic = []

    dic = populate_ponto_medio('diesel_nacional', './resultados_csv/modelo_resultado_diesel_bandeira_nacional.csv', './resultados_csv/resultado_diesel_bandeira_nacional.csv', 'BANDEIRA', 'NACIONAL')
    lista_dic.append(dic)

    dic = populate_ponto_medio('diesel_outro', './resultados_csv/modelo_resultado_diesel_bandeira_outro.csv', './resultados_csv/resultado_diesel_bandeira_outro.csv', 'BANDEIRA', 'OUTRO')
    lista_dic.append(dic)

    dic = populate_ponto_medio('diesel_interior', './resultados_csv/modelo_resultado_diesel_regiao_interior.csv', './resultados_csv/resultado_diesel_regiao_interior.csv', 'REGIÃO', 'INTERIOR')
    lista_dic.append(dic)
    dic = populate_ponto_medio('diesel_metropole', './resultados_csv/modelo_resultado_diesel_regiao_metropole.csv', './resultados_csv/resultado_diesel_regiao_metropole.csv', 'REGIÃO', 'METRÓPOLE')
    lista_dic.append(dic)

    ## --------------

    dic = populate_ponto_medio('diesel_s10_nacional', './resultados_csv/modelo_resultado_diesel_s10_bandeira_nacional.csv', './resultados_csv/resultado_diesel_s10_bandeira_nacional.csv', 'BANDEIRA', 'NACIONAL')
    lista_dic.append(dic)

    dic = populate_ponto_medio('diesel_s10_outro', './resultados_csv/modelo_resultado_diesel_s10_bandeira_outro.csv', './resultados_csv/resultado_diesel_s10_bandeira_outro.csv', 'BANDEIRA', 'OUTRO')
    lista_dic.append(dic)

    dic = populate_ponto_medio('diesel_s10_interior', './resultados_csv/modelo_resultado_diesel_s10_regiao_interior.csv', './resultados_csv/resultado_diesel_s10_regiao_interior.csv', 'REGIÃO', 'INTERIOR')
    lista_dic.append(dic)

    dic = populate_ponto_medio('diesel_s10_metropole', './resultados_csv/modelo_resultado_diesel_s10_regiao_metropole.csv', './resultados_csv/resultado_diesel_s10_regiao_metropole.csv', 'REGIÃO', 'METRÓPOLE')
    lista_dic.append(dic)

    lista_name = []
    lista_k = []
    lista_c = []
    lista_r = []


    for item in lista_dic:
        lista_name.append(item['name'])
        lista_k.append(item['k'])
        lista_c.append(item['c'])
        lista_r.append(item['r'])

    df = pd.DataFrame({'Nome': lista_name, 'Amplitude Total': lista_r, 'Número de Classes': lista_k, 'Amplitude de Classe': lista_c})

    #df.to_csv('./tabelas_variaveis/tabela_variavel.csv')

cria_tabela_var()


# def cria_tabela_variaveis(self):
#     lista_dic = []

#     dic = populate_ponto_medio('diesel_nacional', './csvs_montados/modelo_resultado_bandeira_nacional.csv', './resultados_csv/resultado_diesel.csv', 'REGIÃO', 'INTERIOR')

#     dic = populate_ponto_medio('diesel_nacional', './csvs_montados/modelo_resultado_bandeira_nacional.csv', './resultados_csv/resultado_diesel.csv', 'REGIÃO', 'INTERIOR')

#     dic = populate_ponto_medio('diesel_nacional', './csvs_montados/modelo_resultado_bandeira_nacional.csv', './resultados_csv/resultado_diesel.csv', 'BANDEIRA', 'NACIONAL')

#     dic = populate_ponto_medio('diesel_nacional', './csvs_montados/modelo_resultado_bandeira_nacional.csv', './resultados_csv/resultado_diesel.csv', 'BANDEIRA', 'OUTRO')

#     lista_dic.append(dic)

    