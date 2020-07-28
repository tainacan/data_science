# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 19:46:31 2020

@author: luisr
"""

from selenium import webdriver
import pandas as pd
import random
from collections import defaultdict
import time
result_dict = defaultdict(list)
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
    n = random.randint(1,101810)
    
    print("Acessando o objeto de id {}".format(n))
        
    #Abre a página da URL selecionada
    firefox.get('http://acervo.bndigital.bn.br/sophia/index.asp?codigo_sophia={}'.format(n))

    time.sleep(5)
    #Identifica o frame onde os metadados estão
    frame = firefox.find_element_by_tag_name("frameset").find_element_by_tag_name("frame")
    
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
        #Nesse momento o script dá erro se o numero idnetificador não for encontrado (Previsão de 101.818 itens)
        metadata = firefox.find_element_by_xpath("//*[@class='max_width table-ficha-detalhes']").get_attribute('outerHTML')
        
        print("Transformando os metadados")
        #Tranforma a tabela em um dataframe
        df  = pd.read_html(metadata)
        result_table= df[0]
    
        print("Gravando metadados")
           
        result_table = result_table.dropna()[[1,2]]
        result_table_T = result_table.transpose()
        result_table_T.columns = result_table_T.iloc[0].values
        print(result_table_T['Link do título'][2])
        print(result_table_T.columns)
        
        for column in result_table_T.columns:
            result_dict[column] = result_table_T[column][2]
        
        result_df = result_df.append(result_dict, ignore_index = True)
        
        print("Intervalo de 5 segundos")
        time.sleep(5)
    

    except:
        
        not_find.append(n)
        print("{} Não encontrado".format(n))
        time.sleep(5)
    print(result_dict)

result_df.to_csv("C://Users//luisr//OneDrive//Documentos//funarte_sophia_acervo.csv", index = False)
#%%
print(not_find)