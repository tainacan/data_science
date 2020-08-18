# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 16:50:10 2020

@author: luisr
"""
from selenium import webdriver
import pandas as pd
import random
import time

#Configura o webdriver como Firefox
#Link para donwload do geckodriver do Firefox - https://github.com/mozilla/geckodriver/releases
#Necessita do geckodriver salvo em uma pasta identificada nas variáveis de ambiente PATH.
#(Sugiro salvar na pasta do Python ou do Anaconda)

def sophia_webScrape(entidade, url, n_items):
    
    result_df = pd.DataFrame()
    firefox = webdriver.Firefox()
    not_find = []
    
    for obj_id in range(100):
        
        n = random.randint(1,n_items)
        result_dict = {}
        
        print("\nAcessando o objeto de id {}".format(n))
            
        #Abre a página da URL selecionada
        firefox.get(url + '/index.asp?codigo_sophia={}'.format(n))
                    
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
        
        try:
            print("Identificando metadados")
            #Identifica a tabela com os metadados na tabela com a classe max_width table-ficha-detalhes
            #Nesse momento o script dá erro se o numero idnetificador não for encontrado
            metadata = firefox.find_element_by_xpath("//*[@class='max_width table-ficha-detalhes']").get_attribute('outerHTML')
            
            print("Transoformando os metadados")
            #Tranforma a tabela em um dataframe
            result_table  = pd.read_html(metadata)
            #read_html resulta em um dataframe de dataframes, e a tabela de interesse se encontra do índice 0
            result_table = result_table[0]
        
            print("Gravando metadados")
            #Somente as duas últimas colunas deste dataframe tem os valores de interesse
            result_table = result_table[[1,2]]
            #É necessário executar uma transposição do dataframe, pois o nome das colunas vem na primeira coluna, e os valores na segunda coluna
            result_table_T = result_table.transpose()
            result_table_T.columns = result_table_T.iloc[0].values
            #Essa função elimina as colunas que retornam valor nulo
            result_table_T = result_table_T.drop([1]).dropna(axis='columns',how='all')
            
            
            #Transoforma o dataframe resultante em um dicionário, para posterior inserção dos valores do item em um dataframe
            for column in result_table_T.columns:
                result_dict[column] = result_table_T[column].values[0]
            
            result_dict['Link do Item'] = url + '/index.asp?codigo_sophia={}'.format(n)
            
            result_df = result_df.append(result_dict, ignore_index=True)
    
            print("Intervalo de 5 segundos")
            time.sleep(5)
            
        except Exception as e:
            print(e)
            #Caso o item não seja encontrado ele seu código é armazenado em uma lista
            print("Item {} Não encontrado".format(n))
            not_find.append(n)
            time.sleep(5)
            
    #Csv com dados dos registros coletados
    result_df.to_csv("C://Users//luisr//OneDrive//Documentos//" + entidade + "_sophia_webSpcrape.csv", index = False)
    
    #Txt com os códigos não encontrados
    with open("C://Users//luisr//OneDrive//Documentos//" + entidade + "_notFindCodes.txt", "w") as not_find_txt:
        not_find_txt.write(", ".join(str(code) for code in not_find))
    
    firefox.quit()
    
#%%
nItens_dict = {"funarte||http://cedoc.funarte.gov.br/sophia_web/":125859, 
               "bn_digital||http://acervo.bndigital.bn.br/sophia/":101818, 
               "rui||http://acervos.casaruibarbosa.gov.br/":220911}


for entidade in nItens_dict.keys():
    
    print("\nColetando 100 itens aleatórios de {}".format(entidade.split('||')[0]))
    sophia_webScrape(entidade.split('||')[0], entidade.split('||')[1], nItens_dict[entidade])