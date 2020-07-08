# -*- coding: utf-8 -*-
"""
Created on Wed May  6 21:30:36 2020

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
                                                        
#Some taxonomies arent designated to collections, so we need to made a relationship table for installations, collections and taxonomies

#Truncate Taxonmy table
functions.truncate_table('inst_col_tax')

#Create installation, collection and taxonomy relation dataframe
inst_col_tax_table = pd.DataFrame(columns=tables.dfTables['inst_col_tax'])

#Get taxonomy and collection table from database
taxonomy_db = pd.read_sql_table('taxonomia', dbConnection)
collection_db = pd.read_sql_table('colecao', dbConnection)


#Collect data from installation, collection and taxonomy endpoint on Tainacan API per Installation
for i in range(len(api.install_dict['id'])):
    
    print("Verificando a Instalação {}".format(api.install_dict['name'][i]))
    
    taxonomy_resp = functions.try_request(api.install_dict['url'][i]+api.dict_endpoint['tax_endpoint'])
    paged = 0
    
    #Relation between taxonomies and collection are get by taxonomy endpoint, so we need to repeat the process of get taxonomy data from API.
    while taxonomy_resp.json() != []:
        
        paged += 1
        taxonomy_resp = functions.try_request(api.install_dict['url'][i]+api.dict_endpoint['tax_endpoint']+"/?paged={}".format(paged))

        print("Verificando a página {}".format(paged))
        
        print("Quantidade de Taxonomias {}".format(len(taxonomy_resp.json())))
        
        for taxonomy in taxonomy_resp.json():
            
            db_taxonomy = taxonomy_db.loc[taxonomy_db['name'] == taxonomy['name']]
            
            if db_taxonomy['id'].values.size == 0:
                print("Taxonomia não encontrada do banco de dados")
                continue
            else:
                taxonomy_id = db_taxonomy['id'].values[0]
            
            #Check if a taxonomy have collections using it
            if len(taxonomy['collections_ids']) > 0:
                
                for collection_id in taxonomy['collections_ids']:
                    collection_resp = functions.try_request(api.install_dict['url'][i]+api.dict_endpoint['col_endpoint']+str(collection_id)).json()
                    
                    db_collection = collection_db.loc[collection_db['name'] == collection_resp['name']]
            
                    if db_collection['id'].values.size == 0:
                        print("Coleção não encontrada do banco de dados")
                        continue
                        
                    else:
                        collection_new_id = db_collection['id'].values[0]
                        print('Relacionando instalação {} com coleção {} com taxonomia {}'.format(api.install_dict['name'][i],
                                                                                                 db_collection['name'].values[0],
                                                                                                 db_taxonomy['name'].values[0]))
                        
                        inst_col_tax_table = inst_col_tax_table.append({'id_instalacao':api.install_dict['id'][i],
                                                                        'id_colecao':collection_new_id,
                                                                        'id_taxonomia':taxonomy_id}, ignore_index=True)

print("Escrevendo dados da relação entre instalação, coleções e taxonomia no Banco de Dados")
#Convert the relationship DataFrame to it respective SQL Table
inst_col_tax_table.to_sql('inst_col_tax', dbConnection, if_exists = 'append', chunksize = 1000, index=False)
