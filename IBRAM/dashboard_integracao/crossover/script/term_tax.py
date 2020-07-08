# -*- coding: utf-8 -*-
"""
Created on Wed May  6 21:22:48 2020

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

#Acesso ao banco de dados - Substituir usuário e senha
mysqlEngine = create_engine('mysql+pymysql://user:password@localhost:3306/tainacan_api')
dbConnection = mysqlEngine.connect()

#Truncate Terms table
#functions.truncate_table('tax_term')

#Collect data from terms endpoint on Tainacan API per Installation
terms_table = pd.DataFrame(columns=tables.dfTables['term'])

#Used on hierarchy dealing
termTax_df = pd.DataFrame(columns = tables.dfTables['term_tax'])

#Get taxonomy and term table from database
taxonomy_db = pd.read_sql_table('taxonomia', dbConnection)
terms_db = pd.read_sql_table('termos', dbConnection)

for i in range(len(api.install_dict['id'])):
    
    print("Verificando a Instalação {}".format(api.install_dict['name'][i]))
    
    #Terms are get by taxonomies, so we need to repeat the process of getting taxonomy data above
    taxonomy_resp = functions.try_request(api.install_dict['url'][i]+api.dict_endpoint['tax_endpoint'])
    paged = 0
    
    while taxonomy_resp.json() != []:
        paged += 1
        
        print("Verificando a página {} de taxonomias".format(paged))
        taxonomy_resp = functions.try_request(api.install_dict['url'][i]+api.dict_endpoint['tax_endpoint']+"/?paged={}".format(paged))
        
        for taxonomy in taxonomy_resp.json():
            print("Verificando os termos taxonomia {}".format(taxonomy['name']))
            term_resp = functions.try_request(api.install_dict['url'][i]+api.dict_endpoint["terms_endpoint"].format(taxonomy['id']))
            
            db_taxonomy = taxonomy_db.loc[taxonomy_db['name'] == taxonomy['name']]
            
            if db_taxonomy.size == 0:
                print("Taxonomia não encontrada do banco de dados")
                continue
            else:
                taxonomy_id = db_taxonomy['id'].values[0]
            
            #Taxonomia sem termos
            if term_resp.json() == []:
                continue
            
            else:
                print("Verificando {} termos".format(len(term_resp.json())))

                for term in term_resp.json():
                    db_term = terms_db.loc[terms_db['name'] == functions.normalize(term['name'])]
                    
                    if db_term.size == 0:
                        print("Termo não encontrado no banco de dados")
                        continue
                        
                    else:
                        term_id = db_term['id'].values[0]
                        termTax_df = termTax_df.append({'taxonomy_id':taxonomy_id, 'term_id':term_id}, ignore_index=True)
                        
#Convert the terms DataFrame to it respective SQL Table
print("Escrevendo os termos no Banco de Dados")
termTax_df.to_sql('tax_term', dbConnection, if_exists = 'append', chunksize = 1000, index=False)
