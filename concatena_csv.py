import glob
import os
import pandas as pd


def concatena_tabelas(combustivel):
    first = None
    bool_first = False
    table_list = []

    
    for filename in glob.glob(combustivel + '/*.csv'):
        table = pd.read_csv(filename)
        table.columns = ['RAZÃO SOCIAL', 'ENDEREÇO', 'BAIRRO', 'BANDEIRA','PREÇO VENDA','DATA COLETA']
        table.drop('RAZÃO SOCIAL',inplace=True, axis=1) # Deleta uma coluna
        table.drop('DATA COLETA', inplace=True, axis=1)
        table.drop('ENDEREÇO', inplace=True, axis=1)
        table.drop('BAIRRO', inplace=True, axis=1)

        city_name = filename.replace('.csv', '')
        city_name.replace('_', ' ')
        city_name.split(' ')
        
        new_city_name = ''

        for palavra in city_name:
            palavra.capitalize()
            new_city_name += f'{palavra} '
        new_city_name = new_city_name[:-1].replace(' ','').replace('_',' ').upper()

        

        table.insert(0, 'Município', new_city_name.split("/")[1])
        table.insert(1, 'Estado', 'São Paulo')
        table.insert(2, 'Combustível', new_city_name.split("/")[0])

        without_NaN = table.dropna()[1:]
        new_table = without_NaN.reset_index(drop=True)
        new_table.index.name = 'Posto'
        new_table.index += 1

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
    final_table.to_csv('resultado.csv')
    print(final_table)

concatena_csv(['diesel', 'diesel_s10'])
