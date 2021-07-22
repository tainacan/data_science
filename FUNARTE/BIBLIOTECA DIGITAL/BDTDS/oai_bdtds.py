# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 16:37:51 2021

@author: luisr & érika
"""
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
import pandas as pd
import re
import inspect
import time

result_df = pd.DataFrame()
registry = MetadataRegistry()
registry.registerReader('oai_dc', oai_dc_reader)

bdtd = pd.read_csv('bdtd_unb.csv')
types =  pd.read_csv('types.csv')
#%%
setDataList = [[]]
def join_dict_values(dictionary):
    for key,value in dictionary.items():
        if isinstance(dictionary[key], list):
            dictionary[key] = '||'.join(dictionary[key])
            
def remove_empty_keys(dictionary):

    no_empty_dict = dict()
    valid_value_list = list()

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


with open('erro_log.txt', 'w') as f:

    for i in range(len(bdtd['provider'])):# list the providers urls from csv
        try:
            provider = bdtd['provider'][i].split("(")[1].strip(")")
            url_provider = bdtd['url_provider'][i]
            set_list = bdtd['comunidade'].to_list()[0].split(",")
            print("Acessando os dados de provedor ", provider)    
            print(url_provider)
            
            registry = MetadataRegistry()
            registry.registerReader('oai_dc', oai_dc_reader)
            client = Client(url_provider, registry)
            sets = client.listSets()
            
            for setSpec, setName, setDescription in sets:
                try:
                    
                    if setName.strip() in set_list:
                        records = client.listRecords(metadataPrefix='oai_dc', set=setSpec)
                        print("Coletando dados do conjunto ", setName)
                        count = 1
                        
                        for record in records:
                            header, metadata, about = record
                            
                            if metadata:
                                # getMap return dictonary with all metadata fields
                                doc = metadata.getMap()
                        
                                doc['_id'] = re.sub('[:/.]','-',header.identifier())
                                doc['datestamp'] = str(header.datestamp())
                        
                                # only save documents that have identifier metadata
                                if doc['identifier']:
                                    
                                    if count > 0 and doc['_id'] not in result_df['_id'].to_list():
                                    
                                        join_dict_values(doc)#transformar valores de lista para texto separado por ||
                                    
                                        if doc['type'].lower().strip() in types['type'].to_list():
                                        
                                            print("Coletando dados do registro ", doc['type'])
                                            try:
                                                doc['provider'] = provider
                                                doc['conjunto'] = setName
                                                doc['setSpec'] = setSpec
                                                #print(count)
                                                count +=1
                                                result_df = result_df.append(doc, ignore_index=True)
                                                
                                            except Exception as e:
                                                print(e)
                                                f.write(str(e))
                                                continue
                except Exception as e:
                    print(e)
                    f.write(str(e))
                    continue
        
                result_df.to_csv("resultado_oai_bdtd.csv",index=False)
                
        except Exception as e:
            print(e)
            f.write(str(e))
            continue
