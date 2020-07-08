#!/usr/bin/env python
# coding: utf-8
   
#Required Packages
import requests
import pandas as pd
import time
from datetime import datetime
from collections import defaultdict
from fuzzywuzzy import fuzz

#API Endpoint
api_url = 'https://query.wikidata.org/sparql'
values_df = pd.read_csv("values_database.csv", encoding='utf-8')

#Get the best instance option found for each metadata
instance_df = pd.read_csv('instance_obj.csv', encoding='utf-8')
instance_df = instance_df[instance_df['best_option'] == "x"]

#Create a dict to direct metadata to wikidata instance
instance_dict = {}
for index, row in instance_df.iterrows():
    instance_dict[row['metadado']] = row['qid_instance'].split("/")[-1]
    
def value_wikiObj(instance_input, values):
    reconc_df = pd.DataFrame(columns=["metadado", "instancia", "valor", "qid_valor", "score"])
    
    for column in values.columns:
    
        if column in instance_input.keys():

            start_time = datetime.now()
        
            for index, row in values.iterrows():
                
                score_dict = defaultdict(list)
            
                #Ignore missing values
                if str(row[column]) == 'nan':
                
                    continue

                else:
                
                    if "||" in str(row[column]):
                        
                        for multivalue in str(row[column]).split("||"):
                            score_dict = defaultdict(list)
                            
                            if multivalue in reconc_df['valor'].to_list():
                                continue
                                
                            else:
                                                                
                                query = """ SELECT DISTINCT ?sujeito ?sujeitoLabel ?sujeitoAltLabel WHERE {

                                   { ?sujeito ?label "%s". }
                                  UNION
                                  { ?sujeito ?label "%s"@en. }
                                  UNION
                                  { ?sujeito ?label "%s"@pt-br. }

                                  ?sujeito wdt:P31 wd:%s

                                  SERVICE wikibase:label { bd:serviceParam wikibase:language "pt-br", "pt", "en". }
                                }"""%(multivalue, multivalue, multivalue,instance_input[column])

                                r = requests.get(api_url, params = {'format': 'json', 'query': query})
                                time.sleep(3)
                                
                                tentativas = 0
                                while str(r) != "<Response [200]>":
                                    print(r)
                                    print("Erro no JSON ao coletar o valor {}, tentando novamente em 300 segundos".format(multivalue))
                                    time.sleep(300)
                                    r = requests.get(api_url, params = {'format': 'json', 'query': query})
                                    tentativas +=1
                                    if tentativas > 5:
                                        print("Excedeu o limite de tentativas, passando ao próximo")
                                        break

                                data = r.json()
                                
                                if data['results']['bindings'] == []:

                                    reconc_df = reconc_df.append({'metadado':column, 'instancia':instance_input[column],
                                                                  'valor':multivalue, 'qid_valor':"NI",
                                                                  'label':"NI",'score':"NI"}, ignore_index=True)

                                else:
                                    
                                    for item in data['results']['bindings']:
                                        lista_label=[]
                                                                                
                                        if 'sujeitoAltLabel' in item.keys():
                                            lista_label = item['sujeitoAltLabel']['value'].split(",")
                                            lista_label.append(item['sujeitoLabel']['value'])
                                            lista_label = list(set(lista_label))
                                        else:
                                            lista_label.append(item['sujeitoLabel']['value'])
                                            lista_label = list(set(lista_label))

                                        for label in lista_label:
                                            
                                            score_dict[item['sujeito']['value']].append(fuzz.ratio(multivalue, label))

                                    for key in score_dict.keys():
                                        avg_score = (sum(score_dict[key])/len(score_dict[key]))
                                        
                                        reconc_df = reconc_df.append({'metadado':column, 'instancia':instance_input[column],
                                                                      'valor':multivalue, 'qid_valor':key,
                                                                      'score':avg_score}, ignore_index=True)
                    else:
                        
                        if row[column] in reconc_df['valor'].to_list():
                            
                            continue
                            
                        else:
                            
                            query = """ SELECT DISTINCT ?sujeito ?sujeitoLabel ?sujeitoAltLabel WHERE {

                                  { ?sujeito ?label "%s". }
                                  UNION
                                  { ?sujeito ?label "%s"@en. }
                                  UNION
                                  { ?sujeito ?label "%s"@pt-br. }

                                  ?sujeito wdt:P31 wd:%s

                                  SERVICE wikibase:label { bd:serviceParam wikibase:language "pt-br", "pt", "en". }
                                }"""%(row[column], row[column], row[column],instance_input[column])

                            r = requests.get(api_url, params = {'format': 'json', 'query': query})
                            time.sleep(3)
                            
                            tentativas = 0
                            while str(r) != "<Response [200]>":
                                print(r)
                                print("Erro no JSON ao coletar o valor {}, tentando novamente em 300 segundos".format(row[column]))
                                time.sleep(300)
                                r = requests.get(api_url, params = {'format': 'json', 'query': query})
                                tentativas +=1
                                
                                if tentativas > 5:
                                    print("Excedeu o limite de tentativas, passando ao próximo")
                                    break
                                
                            data = r.json()

                            if data['results']['bindings'] == []:
                                
                                reconc_df = reconc_df.append({'metadado':column, 'instancia':instance_input[column],
                                                                  'valor':row[column], 'qid_valor':"NI",
                                                                  'label':"NI",'score':"NI"}, ignore_index=True)

                            else:
                                
                                for item in data['results']['bindings']:
                                    lista_label=[]
                                    
                                    if 'sujeitoAltLabel' in item.keys():
                                        lista_label = item['sujeitoAltLabel']['value'].split(",")
                                        lista_label.append(item['sujeitoLabel']['value'])
                                        lista_label = list(set(lista_label))
                                    else:
                                        lista_label.append(item['sujeitoLabel']['value'])
                                        lista_label = list(set(lista_label))

                                    for label in lista_label:
                                        
                                        score_dict[item['sujeito']['value']].append(fuzz.ratio(row[column], label))

                                for key in score_dict.keys():
                                    
                                    avg_score = (sum(score_dict[key])/len(score_dict[key]))
                                        
                                    reconc_df = reconc_df.append({'metadado':column, 'instancia':instance_input[column],
                                                                'valor':row[column], 'qid_valor':key,
                                                                'score':avg_score}, ignore_index=True)
                                        
            print("Valores verificados em {} para o metadado {}".format(datetime.now()-start_time, column))

    return reconc_df

value_wikiObj(instance_dict,values_df).to_csv("teste_valores.csv")
