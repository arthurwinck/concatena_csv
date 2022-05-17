import glob
import os
import pandas as pd
import numpy as np



from extract_cities import extract_cities


def concatena_tabelas(combustivel):
    first = None
    bool_first = False
    table_list = []

    
    for filename in glob.glob(combustivel + '/*.csv'):
        table = pd.read_csv(filename, encoding='latin-1')
        table.columns = ['RAZÃO SOCIAL', 'ENDEREÇO', 'BAIRRO', 'BANDEIRA','PREÇO VENDA','DATA COLETA']
        table.drop('RAZÃO SOCIAL',inplace=True, axis=1) # Deleta uma coluna
        table.drop('DATA COLETA', inplace=True, axis=1)
        table.drop('ENDEREÇO', inplace=True, axis=1)
        table.drop('BAIRRO', inplace=True, axis=1)


        # Nomear as cidades a partir do nome do arquivo
        city_name = filename.replace('.csv', '')
        city_name.replace('_', ' ')
        city_name.split(' ')
        
        new_city_name = ''

        for palavra in city_name:
            palavra.capitalize()
            new_city_name += f'{palavra} '
        new_city_name = new_city_name[:-1].replace(' ','').replace('_',' ').upper()

        table.insert(0, 'MUNICÍPIO', new_city_name.split("\\")[1])
        table.insert(1, 'ESTADO', 'SÃO PAULO')
        table.insert(2, 'COMBUSTÍVEL', new_city_name.split("\\")[0])

        # Adicionar coluna de metrópole a partir da função extract_cities
        city_list = extract_cities('table.txt')

        if new_city_name.split("\\")[1] in city_list:
            table.insert(5, 'REGIÃO', 'METRÓPOLE')
        else:
            table.insert(5, 'REGIÃO', 'INTERIOR')


        # Renomear bandeiras para entrar no padrão de nacional ou outro
        for i in range(len(table['BANDEIRA'])):
            if table['BANDEIRA'][i] in ['VIBRA ENERGIA','VIBRASAT','IPIRANGA','TAURUS','ALESAT']:
                table['BANDEIRA'][i] = "NACIONAL"
            else:
                table['BANDEIRA'][i] = "OUTRO"


        without_NaN = table.dropna()[1:]
        new_table = without_NaN.reset_index(drop=True)
        new_table.index.name = 'POSTO'
        new_table.index += 1
        
        # Ajustar preços que não possuem vírgula
        for i in range(1, len(new_table['PREÇO VENDA']) + 1):
            if isinstance(new_table['PREÇO VENDA'][i], str):
                if ',' in new_table['PREÇO VENDA'][i]:
                    new_table['PREÇO VENDA'][i] = new_table['PREÇO VENDA'][i].replace(',', '')

                new_table['PREÇO VENDA'][i] = int(new_table['PREÇO VENDA'][i])
                
            #converter pra string checar quantos caracteres tem e dale --> ruim e lento :(
            # Fazer o log de 10 do número -> rápido mas tem que botar biblioteca :)

             #np.log10(15000) -> 4.056234
            decimal_houses = np.round(np.log10(new_table['PREÇO VENDA'][i])) 
            new_table['PREÇO VENDA'][i] = new_table['PREÇO VENDA'][i]*10**(3-decimal_houses)/10**2


        if bool_first:
            table_list.append(new_table)
        else:
            bool_first = True
            first = new_table
    
    parcial_table = pd.concat(table_list)
    return parcial_table

def concatena_csv(lista_combustivel):
    final_table_list = []


    for comb in lista_combustivel:
        parcial_table = concatena_tabelas(comb)
        final_table_list.append(parcial_table)
    
    final_table = pd.concat(final_table_list)
    final_table.to_csv(f'resultado_{lista_combustivel[0]}.csv')
    print(final_table)

concatena_csv(['diesel'])
concatena_csv(['diesel_s10'])
