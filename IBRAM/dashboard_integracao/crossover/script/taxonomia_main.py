# -*- coding: utf-8 -*-
"""
Created on Wed May  6 21:29:06 2020

@author: luisr
"""
#Internal path structure 
import sys
#Adicionar o path do diretório contendo os scripts
sys.path.append('')
from dicts import api_access as api, tables
import functions
import pandas as pd
from sqlalchemy import create_engine

#Acesso ao banco de dados. Substituir o usuário e a senha.
mysqlEngine = create_engine('mysql+pymysql://user:password@localhost:3306/tainacan_api')
dbConnection = mysqlEngine.connect()

#Collect data from taxonomy endpoint on Tainacan API per Installation
#Truncate Taxonmy table
#functions.truncate_table('taxonomia')

#Cria dataframe com as colunas da tabela de taxonomia
taxonomies_table = pd.DataFrame(columns=tables.dfTables['taxonomy'])


for i in range(len(api.install_dict['id'])):
    
    print("Verificando a instalação {}".format(api.install_dict['name'][i]))
    
    taxonomy_resp = functions.try_request(api.install_dict['url'][i]+api.dict_endpoint['tax_endpoint'])
    paged = 0
        
    #The response of API came in a interval of 10 results perpage, we used while to interate between the result pages, until there is no more result to show
    while taxonomy_resp != []:
        
        paged += 1
        print("Verificando a página {} de taxonomias".format(paged))
        taxonomy_resp = functions.try_request(api.install_dict['url'][i]+api.dict_endpoint['tax_endpoint']+"/?paged={}".format(paged)).json()
        
        for taxonomy in taxonomy_resp:
            
            print("Verificando a taxonomia {}".format(taxonomy['name']))
            if taxonomy['name'] in taxonomies_table['name'].to_list():
                continue
            else:
                taxonomies_table = taxonomies_table.append({'name':taxonomy['name'], 'description': taxonomy['description'],
                                                            'allow_insert': taxonomy['allow_insert']}, ignore_index=True)

#Convert the taxonomy DataFrame to it respective SQL Table
print("Escrevendo os dados de taxonomias no Banco de Dados")
taxonomies_table.to_sql('taxonomia', dbConnection, if_exists = 'append', chunksize = 1000, index=False)
