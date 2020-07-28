# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 12:02:49 2020

@author: luisr
"""

from selenium import webdriver
import pandas as pd
import random
from collections import defaultdict
import time
result_dict = defaultdict(list)
result_df = pd.DataFrame(columns = ['jpg', 'pdf', 'CDD', 'Imprenta', 'Outros títulos', 'Série', 'Periodicidade', 'Descrição original', 'Gerais', 'MP3', 'Meio eletrônico', 'Colaborador', 'Notas', 'Locais 6', 'Fonte', 'Locais', 'Forma fís. adicional', 'Título', 'Custódia', 'Link do título', 'Sites relacionados', 'HTM', 'Citação/referência', 'Autor/Criador', 'Coleção', 'Locais 8', 'HTML', '"Com"', 'Assuntos', 'PDF', 'Fonte - Obra', 'Site', 'Loc. original', 'Tipo de documento', 'Título analítico fonte', 'Título não controlado', 'JPG', 'ContentE', 'Reprodução', 'htm', 'Número de chamada', 'Idioma'])

#Configura o webdriver como Firefox
#Link para donwload do geckodriver do Firefox - https://github.com/mozilla/geckodriver/releases
#Necessita do geckodriver salvo em uma pasta identificada nas variáveis de ambiente PATH.
#(Sugiro salvar na pasta do Python ou do Anaconda)

firefox = webdriver.Firefox()
not_find = []

for obj_id in range(100):
    
    result_dict = {}
    print(result_dict)
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
        
        print("Transoformando os metadados")
        #Tranforma a tabela em um dataframe
        df  = pd.read_html(metadata)
        result_table= df[0]
    
        print("Gravando metadados")
            
        print("Intervalo de 5 segundos")
        time.sleep(5)
    


            
        result_table = result_table.dropna()[[1,2]]
        result_table_T = result_table.transpose()
        result_table_T.columns = result_table_T.iloc[0].values
        print(result_table_T['Link do título'][2])
        
        for column in result_df.columns:
            if column in result_table_T.columns:
                result_dict[column] = result_table_T[column][2]
            
            else:
                result_dict[column] = ''
        
        print(result_dict['Link do título'])
    
        print("Inserindo metadados e valores")
        
        result_df = result_df.append({'jpg':result_dict['jpg'],'pdf':result_dict['pdf'],'CDD':result_dict['CDD'],
                                          'Imprenta':result_dict['Imprenta'],'Outros títulos':result_dict['Outros títulos'],
                                          'Série':result_dict['Série'],'Periodicidade':result_dict['Periodicidade'],
                                          'Descrição original':result_dict['Descrição original'],'Gerais':result_dict['Gerais'],
                                          'MP3':result_dict['MP3'],'Meio eletrônico':result_dict['Meio eletrônico'],
                                          'Colaborador':result_dict['Colaborador'],'Notas':result_dict['Notas'],
                                          'Locais 6':result_dict['Locais 6'],'Fonte':result_dict['Fonte'],
                                          'Locais':result_dict['Locais'],'Forma fís. adicional':result_dict['Forma fís. adicional'],
                                          'Título':result_dict['Título'],'Custódia':result_dict['Custódia'],
                                          'Link do título':result_dict['Link do título'],'Sites relacionados':result_dict['Sites relacionados'],
                                          'HTM':result_dict['HTM'],'Citação/referência':result_dict['Citação/referência'],
                                          'Autor/Criador':result_dict['Autor/Criador'],'Coleção':result_dict['Coleção'],
                                          'Locais 8':result_dict['Locais 8'],'HTML':result_dict['HTML'],'"Com"':result_dict['"Com"'],
                                          'Assuntos':result_dict['Assuntos'],'PDF':result_dict['PDF'],'Fonte - Obra':result_dict['Fonte - Obra'],
                                          'Site':result_dict['Site'],'Loc. original':result_dict['Loc. original'],
                                          'Tipo de documento':result_dict['Tipo de documento'],'Título analítico fonte':result_dict['Título analítico fonte'],
                                          'Título não controlado':result_dict['Título não controlado'],'JPG':result_dict['JPG'],
                                          'ContentE':result_dict['ContentE'],'Reprodução':result_dict['Reprodução'],'htm':result_dict['htm'],
                                          'Número de chamada':result_dict['Número de chamada'],'Idioma':result_dict['Idioma']}, ignore_index = True)

    except:
        
        not_find.append(n)
        print("{} Não encontrado".format(n))
        time.sleep(5)

result_df.to_csv("bn_acervo_teste.csv", index = False)
