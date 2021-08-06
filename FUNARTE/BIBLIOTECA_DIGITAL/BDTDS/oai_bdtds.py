# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 16:37:51 2021

@author: luisr & Érika
"""
#Script desenvolvido para coletar os dados de provedores OAI-PMH.
#São coletados Teses, Dissertações e Livros de programas de pós-graduação
#em artes.

#biblioteca para acessar o OAI-PMH - pyoai
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
import pandas as pd
import re
from datetime import datetime

result_df = pd.read_csv('resultado_oai_bdtd_columns.csv')
registry = MetadataRegistry()
registry.registerReader('oai_dc', oai_dc_reader)

bdtd = pd.read_csv('BDTDS_CONJUNTOS.csv')#le o arquivo com as informações dos provedores
types =  pd.read_csv('types.csv')#le o arquivo com os data types
#%%
def join_dict_values(dictionary): #transofrma as listas em string e une os valores por ||
    for key,value in dictionary.items():
        if isinstance(dictionary[key], list):
            dictionary[key] = '||'.join(dictionary[key])

def remove_empty_keys(dictionary):#remove metadados com valores vazios

    no_empty_dict = dict()
    #valid_value_list = list()

    for key,value in dictionary.items():
        if value:
            if isinstance(value, list) and len(value) > 0:
                valid_values_list = [v for v in value if v != 'None']
                if valid_values_list:
                    no_empty_dict[key] = valid_values_list
            else:
                if value != 'None':
                    no_empty_dict[key] = value

    return no_empty_dict

with open('erro_log.txt', 'w') as f: #abre um arquivo de texto para armazenar os erros da coleta

    for i in range(len(bdtd['provider'])):# percorre a planilha dos provedores
    
        provider = bdtd['provider'][i]#armazena a sigla da instituição
        url_provider = bdtd['url_provider'][i]#armazena a url do provedor
        set_list = bdtd['setSpec'][i].split(",")#recupera as comunidades a serem coletadas
        print(provider, set_list)
        

        try:
            
            print("Acessando os dados de provedor ", provider)
            
            #Conecta com o provedor OAI-PMH
            registry = MetadataRegistry()
            registry.registerReader('oai_dc', oai_dc_reader)
            client = Client(url_provider, registry)
            
            #sets = client.listSets()#lista os conjuntos
            
            for setSpec in set_list: #percorre cada conjunto do provedor

                try:
                    
                    if str(setSpec).strip() in set_list: #verifica se o conjunto está na lista dos selecionados
                    
                        print("********CONJUNTO ENCONTADO***********")
                    
                        records = client.listRecords(metadataPrefix='oai_dc', set=setSpec)#lista os registros
                        
                        print("Coletando dados do conjunto {}, do provedor {} \n".format(setSpec, provider))
                        
                        count = 1
                        
                        for record in records:#percorre os registros
                            header, metadata, about = record
                            
                            if metadata:
                                #getMap return dictonary with all metadata fields
                                doc = metadata.getMap()
                        
                                doc['_id'] = re.sub('[:/.]','-',header.identifier())
                                doc['datestamp'] = str(header.datestamp())
                        
                                #only save documents that have identifier metadata
                                if doc['identifier']:
                                    join_dict_values(doc)#transformar valores de lista para texto separado por ||
                                    
                                    if doc['_id'] in result_df['_id'].unique():#Verifica se o registro já foi inserido na base
                                        print("Registro já adicionado")
                                        continue
                                    
                                    else:
                                        print("Coletando dados do registro ", doc['type'])
                                        
                                        try:
                                            doc['provider'] = provider
                                            doc['setSpec'] = setSpec
                                            #print(count)
                                            count +=1
                                            print("Coletando registro ",count)
                                            
                                            result_df = result_df.append(doc, ignore_index=True)#armazena o registro em um DataFrame
                                            
                                        except Exception as e:
                                            print(e)
                                            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                            f.write("{} -- ** {} ** - Erro de coleta de registro -- Conjunto {} -- Provedor {}\n".format(dt_string,str(e),setSpec,provider ))
                                            continue
                except Exception as e:
                    print(e)
                    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    f.write("{} -- ** {} ** - Erro de coleta de conjunto -- Conjunto {} -- Provedor {}\n".format(dt_string, str(e),setSpec,provider))
                    continue
                result_df.to_csv("resultado_oai_bdtd.csv",index=False)#salva os dados coletados à cada conjunto
                
        except Exception as e:
            print(e)
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            f.write("{} -- ** {} ** - Erro de coleta de provedor -- Provedor {}\n".format(dt_string, str(e),provider))
            continue
