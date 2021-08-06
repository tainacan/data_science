# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 16:37:51 2021
@author: luisr & Erika(UnB)
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


result_df = pd.read_csv('resultado_oai_periodicos_columns.csv')
registry = MetadataRegistry()
registry.registerReader('oai_dc', oai_dc_reader)

journals = pd.read_csv('periodicos.csv')#le o arquivo com as informações dos provedores
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


#%%
with open('erro_log.txt', 'w', encoding="utf-8") as f: #abre um arquivo de texto para armazenar os erros da coleta

    for i in range(len(journals['issn'])):#percorre a planilha dos provedores
    
        provider_name = journals['titulo'][i]#
        url_provider = journals['url'][i]#armazena a url do provedor
        provider_issn = journals['issn'][i]#
        print(provider_name, url_provider)
        

        try:
            
            print("Acessando os dados de provedor ", provider_name)
            
            #Conecta com o provedor OAI-PMH
            registry = MetadataRegistry()
            registry.registerReader('oai_dc', oai_dc_reader)
            client = Client(url_provider, registry)
            
            print("Conexão estabelecida")
            sets = client.listSets()#lista os conjuntos
            print("Conjuntos encontrados")
            
            for setSpec, setName, setDescription in sets: #percorre cada conjunto do provedor

                try:
                    
                    records = client.listRecords(metadataPrefix='oai_dc', set=setSpec)#lista os registros
                        
                    print("Coletando dados do conjunto {}, do provedor {} \n".format(setName, provider_name))
                    
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
                                        doc['titulo']  = provider_name
                                        doc['issn']    = provider_issn
                                        doc['setSpec'] = setSpec
                                        doc['setName'] = setName
                                       
                                        count +=1
                                        print("Coletando registro ",count)
                                        
                                        result_df = result_df.append(doc, ignore_index=True)#armazena o registro em um DataFrame
                                        
                                    except Exception as e:
                                        print(e)
                                        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                        f.write("{} -- ** {} ** - Erro de coleta de registro -- Conjunto {} -- Provedor {}\n".format(dt_string,str(e),setSpec,provider_name))
                                        continue
                except Exception as e:
                    print(e)
                    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    f.write("{} -- ** {} ** - Erro de coleta de conjunto -- Conjunto {} -- Provedor {}\n".format(dt_string, str(e),setSpec,provider_name))
                    continue
                result_df.to_csv("resultado_oai_bdtd.csv",index=False)#salva os dados coletados à cada conjunto
                
                
        except Exception as e:
            print(e)
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            f.write("{} -- ** {} ** - Erro de coleta de provedor -- Provedor {}\n".format(dt_string, str(e),provider_name))
            continue
