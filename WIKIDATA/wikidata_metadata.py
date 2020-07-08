#!/usr/bin/env python
# coding: utf-8

# # Script to map metadata to wikidata entities (instance of)

# This script uses SPARQL Wikidata API endpoint, and searchs the values of a database (csv file) to determine to wich instance this values belongs. This provide 3 possible wikidata entities that represents each metadatas/columns of the inputed database.

#Required Packages
import requests
import pandas as pd
import time
from datetime import datetime

#API Endpoint
api_url = 'https://query.wikidata.org/sparql'

#Values to reconcile database
tabela_df = pd.read_csv('base_mhn_teste.csv', encoding='utf-8')


def instance_metadata(database):
    
    #Dataframe to store results
    wikiObj_df = pd.DataFrame(columns = ['metadado','instance_label','qid_instance'])
    result_df = pd.DataFrame(columns = ['metadado','instance','qid_instance','ocurrences', 'best_option'])

    #For each metadata/column on values to reconcile database
    for column in database.columns:
        start_time = datetime.now()
        
        print("Verificando o metadado {}".format(column))
        
        value_count = 0
        unique_list = []
        
        #Remove duplicated values
        for value in tabela_df[column].dropna():
            
            if "||" in value:
                
                for multivalue in value.split("||"):
                    
                    unique_list.append(multivalue)
                    
            else:
                
                unique_list.append(value)
        
        #For each value of a column/metadata
        for value in list(set(unique_list)):        
                                        
                #SPARQL query. Returns subject QID, instance QID and instance label, searching the value for subjects
                #with matching labels.
                query = """ SELECT DISTINCT ?sujeito ?instancia_de_que ?instancia_de_queLabel WHERE {
                              { ?sujeito ?label "%s". }
                              UNION
                              { ?sujeito ?label "%s"@en. }
                              UNION
                              { ?sujeito ?label "%s"@pt-br. }
                              ?sujeito wdt:P31 ?instancia_de_que.
                              FILTER(?instancia_de_que NOT IN(wd:Q4167836, wd:Q4167410))
                              SERVICE wikibase:label { bd:serviceParam wikibase:language "pt-br", "pt", "en". }
                            }""" %(value, value, value)
                
                #Request the query to wikidata api and outputs a json.
                r = requests.get(api_url, params = {'format': 'json', 'query': query})
                data = r.json()
                
                #Verify if the JSON returns any data
                if data == None:
                    
                    continue
                
                else:
    
                    #For each result inset data on wikiObj_df
                    for item in data['results']['bindings']:
                        
                        wikiObj_df = wikiObj_df.append({'metadado':column,
                                                      'instance_label':item['instancia_de_queLabel']['value'],
                                                      'qid_instancia':item['instancia_de_que']['value']}, ignore_index=True)
                #Wait 3 seconds to avoid API block
                time.sleep(3)
                
                value_count+=1
                
        print("{} valores verificados em {} para o metadado {}".format(value_count, datetime.now()-start_time, column))

    #Create a new dataframe with data about metadata, wikidata instance, wikidata instance QID, and the most 5 frequent instances. 
    for metadado in list(set(wikiObj_df['metadado'])):
        
        meta_df = wikiObj_df[wikiObj_df['metadado'] == metadado]
        
        for index, value in meta_df['qid_instancia'].value_counts().head(5).items():
            
            meta_df_idx = meta_df.index[meta_df['qid_instancia'] == index][0]
            
            result_df = result_df.append({'metadado':meta_df.at[meta_df_idx,'metadado'],
                                         'instance':meta_df.at[meta_df_idx,'instance_label'],
                                         'qid_instance':meta_df.at[meta_df_idx,'qid_instancia'],
                                         'ocurrences':value, 'best_option':''}, ignore_index=True)
    return result_df

instance_metadata(tabela_df).to_csv("instance_obj.csv", index = False)
