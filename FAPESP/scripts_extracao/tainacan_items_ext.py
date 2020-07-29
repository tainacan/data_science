# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 14:49:22 2020

@author: luisr
"""
import pandas as pd
import requests


def tainacan_ext(install, output_name):
    
    col_endpoint = install+"/wp-json/tainacan/v2/collections/"
    col_r = requests.get(col_endpoint).json()
    
    for col in col_r:
        
        col_name = col['name']
        col_id = col['id']
        items_df = pd.DataFrame()
        
        print("\nColetando 100 itens da coleção {}".format(col_name))
              
        for i in range(3):
            
            print("   * Coletando a página {} de itens".format(i))
            
            items_endpoint = install+"/wp-json/tainacan/v2/collection/{}/items/?perpage=25".format(col_id)
            item_r = requests.get(items_endpoint).json()
            
            if item_r == []:
                 print("   * Todos os itens da coleção {} coletados".format(col_name))
                
            else:
                
                if type(item_r) == dict:
                    
                    item_r = item_r['items']
                        
                for item in item_r:
                        
                    result_dict = {}
                        
                    for metadata in item['metadata'].keys():
                            
                        metadado = item['metadata'][metadata]['name']
                        value = item['metadata'][metadata]['value_as_string']
                            
                        result_dict[metadado] = value
                            
                    items_df = items_df.append(result_dict, ignore_index=True)
                            
                    i += 1
                        
                    if i == 3:
                            
                        print("   * Finalizando coleta de 25 itens da coleção {}".format(col_name))
                            
        print("   * Salvando os itens da coleção {}".format(col_name))
        items_df.to_csv("C://Users//luisr//OneDrive//Documentos//"+output_name+"_{}_ext.csv".format(col_name), index=False)
    
tainacan_ext("http://museudearqueologiadeitaipu.museus.gov.br/", "IBRAM_Itaipu")