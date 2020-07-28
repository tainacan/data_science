# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 11:27:50 2020

@author: luisr
"""
from selenium import webdriver
import pandas as pd
import random
import time
result_df = pd.DataFrame()
#%%
#Configura o webdriver como Firefox
#Link para donwload do geckodriver do Firefox - https://github.com/mozilla/geckodriver/releases
#Necessita do geckodriver salvo em uma pasta identificada nas variáveis de ambiente PATH.
#(Sugiro salvar na pasta do Python ou do Anaconda)

firefox = webdriver.Firefox()
not_find = []

metadata_list = []
for obj_id in range(100):
    
    result_dict = {}
    n = random.randint(1,220911)
    
    print("\nAcessando o objeto de id {}".format(n))
        
    #Abre a página da URL selecionada
    url = 'http://acervos.casaruibarbosa.gov.br/index.asp?codigo_sophia={}'.format(n)
    firefox.get(url)

    time.sleep(5)
    #Identifica o frame onde os metadados estão
    frame = firefox.find_element_by_tag_name("frameset").find_element_by_xpath("//*[@id='mainFrame']")
    
    #Direciona o drives para dentro do conteúdo do frame onde os metadados estão
    firefox.switch_to.frame(frame)
    
    try:
        #Direciona o driver para a div onde a tabela com os metadados está!
        firefox.find_element_by_xpath("//*[@id='div_conteudo']")
        
    except:
        print("Div de conteudo do objeto {} não encontrada".format(n))
        time.sleep(10)
        #Direciona o driver para a div onde a tabela com os metadados está!
        firefox.find_element_by_xpath("//*[@id='div_conteudo']")
    
    print("Identificando metadados")
    try:
        #Identifica a tabela com os metadados na tabela com a classe max_width table-ficha-detalhes
        #Nesse momento o script dá erro se o numero idnetificador não for encontrado
        metadata = firefox.find_element_by_xpath("//*[@class='max_width table-ficha-detalhes']").get_attribute('outerHTML')
               
    
    
        print("Transformando os metadados")
        
        #Tranforma a tabela em um dataframe
        df  = pd.read_html(metadata)
        result_table= df[0]
        
        print("Gravando metadados")
        
        result_table = result_table.dropna()[[1,2]]
        result_table_T = result_table.transpose()
        result_table_T.columns = result_table_T.iloc[0].values
        
        for column in result_table_T.columns:
            result_dict[column] = result_table_T[column][2]
            
        result_dict['Link'] = url
            
        result_df = result_df.append(result_dict, ignore_index = True)
            
        print("Intervalo de 5 segundos")
        time.sleep(5)
    
    except:
        not_find.append(n)
        print("{} Não encontrado".format(n))
        continue

result_df.to_csv("C://Users//luisr//OneDrive//Documentos//rui_sophia_acervo.csv", index = False)
#%%
print(not_find)