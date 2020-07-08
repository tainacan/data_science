# -*- coding: utf-8 -*-
"""
Created on Wed May  6 21:22:48 2020

@author: luisr
"""
#Internal path structure 
import sys
#Adicionar o path do diretório contendo os scripts
sys.path.append('')
from dicts import api_access as api,tables
import functions
import pandas as pd
from sqlalchemy import create_engine

#Acesso ao banco de dados - Substituir usuário e senha
mysqlEngine = create_engine('mysql+pymysql://user:password@localhost:3306/tainacan_api')
dbConnection = mysqlEngine.connect()


                                                                            ##Termos##
#Truncate Terms table
#functions.truncate_table('termos')

#Collect data from terms endpoint on Tainacan API per Installation
terms_table = pd.DataFrame(columns=tables.dfTables['term'])

#Used on hierarchy dealing
parent_df = pd.DataFrame(columns=["term_id", "parent_id"])
passed_terms = []
term_id = 0

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
            term_resp = functions.try_request(api.install_dict['url'][i]+api.dict_endpoint["terms_endpoint"].format(taxonomy['id'])).json()
            
            if term_resp == []:
                continue
            else:
                print("Verificando {} termos".format(len(term_resp)))
                
                for term in term_resp:
                    if functions.normalize(term['name']) in terms_table['name'].values:
                        continue
                    
                    else:
                        term_id += 1
                        terms_table = terms_table.append({'id':term_id, 'name':functions.normalize(term['name']), 'description':term['description'],
                                                          'url':term['url'],'url_imagem':term['header_image'], 
                                                          'parent':term['parent']}, ignore_index=True)
                        

                #Dealing with term hierarchy
                #print("Trabalhando nas hierarquias dos termos da taxonomia {}".format(taxonomy['name']))
                for index, value in terms_table['parent'].items():
                    
                    if terms_table.at[index,'id'] in passed_terms:
                        continue
                        
                    else:
                        
                        if value == 0 or str(value) == 'nan':
                            continue
                    
                        else:
                            print(api.install_dict['url'][i]+api.dict_endpoint["term_endpoint"].format(taxonomy['id'],value))
                            parent_resp = functions.try_request(api.install_dict['url'][i]+api.dict_endpoint["term_endpoint"].format(taxonomy['id'],value)).json()
                                
                            if terms_table.loc[terms_table['name'] == functions.normalize(parent_resp['name'])].index.size == 0:
                                print(terms_table.loc[terms_table['name'] == functions.normalize(parent_resp['name'])].index)
                                print(functions.normalize(parent_resp['name']), "Não está em:")
                                print(terms_table['name'].values)
                                continue
    
                            else:
                                #Locate the term id correspondent to Tainacan parent id
                                index_term = terms_table.loc[terms_table['name'] == functions.normalize(parent_resp['name'])].index[0]
                                new_parent_id = terms_table.at[index_term, 'id']
                                print("Verificando o termo {} é filho do termo {}".format(terms_table.at[index,'name'], terms_table.at[index_term, 'name']))

                                parent_df = parent_df.append({'term_id':terms_table.at[index,'id'],
                                                            'parent_id':new_parent_id}, ignore_index=True)
                            
                    passed_terms.append(terms_table.at[index,'id'])

for term_id in terms_table['id'].to_list():
    if term_id in parent_df['term_id'].to_list():
        parent_index = parent_df.loc[parent_df['term_id'] == term_id].index[0]
        parent_id = parent_df.at[parent_index, 'parent_id']

        term_index = terms_table.loc[terms_table['id'] == term_id].index[0]
        terms_table.at[term_index, 'parent'] = parent_id

#Convert the terms DataFrame to it respective SQL Table
print("Escrevendo os termos no Banco de Dados")
terms_table.to_sql('termos', dbConnection, if_exists = 'append', chunksize = 1000, index=False)
