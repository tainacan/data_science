import pandas as pd
import requests
from time import sleep

install = ""

def taiancan_ext(install):
    

    if "www." in install:
        install_name =  install.split("/")[2].split(".")[1]
    else:
        install_name =  install.split("/")[2].split(".")[0]
        
    #Dicionarios/Dataframes
    colDict = {}
    
    #Tratanto Coleções
    col_endpoint = install+"/wp-json/tainacan/v2/collections/"
    col_r = requests.get(col_endpoint).json()
    
    
    for col in col_r:
        colDict[col['name']] = [col['id'], col['total_items']['publish']]

    for colecao in colDict.keys():
        
        items_df = pd.DataFrame()
        print("Coletando {} itens da coleção {}".format(colDict[colecao][1],colecao))
        for i in range(int(colDict[colecao][1])):
            
            i += 1
            print("Verificando a página {} de itens".format(i))
            
            items_endpoint = install+"/wp-json/tainacan/v2/collection/{}/items/?perpage=25&paged={}".format(colDict[colecao][0], i)
            item_r = requests.get(items_endpoint).json()
            
            if item_r["items"] == []:
                
                print("   * Todos os itens da coleção {} coletados".format(colecao))
                
                break
                
            elif type(item_r) == dict:
                
                item_r = item_r['items']
                    
                for item in item_r:
                        
                    result_dict = {}
                        
                    for metadata in item['metadata'].keys():
                        
                        #Metadados e Valores
                        atributo = item['metadata'][metadata]['name']
                        value = item['metadata'][metadata]['value_as_string']
                        
                        if value == "":
                            continue
                        else:
                            result_dict[atributo] = value
                    
                    #Link do Item no Tainacan
                    result_dict['Link do Item'] = item['url']
                    #Link do Documento
                    result_dict['Document'] = item['document']
                    
                    items_df = items_df.append(result_dict, ignore_index=True)
            sleep(5)
            
        items_df.to_csv("{}_{}.csv".format(install_name,colecao))

taiancan_ext(install)
