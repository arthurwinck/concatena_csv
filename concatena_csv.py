import glob
import os
import tabnanny
import pandas as pd


def concatena_csv(combustivel):
    tabela = pd.Dataframe()

    for filename in glob.glob('*.csv'):
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            gas_csv = pd.read_csv(f)
            
            #Fazer alterações

        
concatena_csv('Diesel')

