# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 14:56:53 2020

@author: robson
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
import urllib3
urllib3.disable_warnings()

#Definindo variáveis
colunas          = ['Nome','Condição', 'Categoria', 'Abrangência', 'UF', 'Município', 'Coordenada(s)_geográfica(s)', 'Quantidade_de_imagens', 'Quantidade_de_videos',
                    'Quantidade_de_audios','Descrição_do_bem_imaterial','Localização_específica','Ações_vinculados_Tipo','Ações_vinculados_Nome','Ações_vinculados_Instrumento',
                    'Ações_vinculados_Situação','Área_de_ocorrência_UF','Área_de_ocorrência_Municípios','Página']
#colunas          = ['Nome','Condição', 'Categoria', 'Abrangência', 'UF', 'Município', 'Coordenada(s) geográfica(s)', 'Quantidade de imagens', 'Quantidade de videos',
#                    'Quantidade de audios','Descrição','Página']
url_base         = "https://sicg.iphan.gov.br/sicg/bemImaterial/rel/"
clases           = ['acaoInst','m']
qtd_link         = 643 #quandtidade de sites que vão ser raspados 643
df               = pd.DataFrame(columns=colunas)


for links in range(1,qtd_link):
    
    url              = (url_base + "%s/" %(links))
    site             = requests.get(url, verify=False)
    soup             = bs(site.text, 'html.parser')
    colunas_label    = soup.find_all('label')[:10]
    result_dict      = {}
    registro         = []
    
    #Verifica se o link está no ar!
    if site.status_code in range(200,300):
        
        print('Acesando os dados do link:', format(url))
        
        for lista_colunas in colunas_label:        
            registro.append(lista_colunas.find_next_sibling("div").getText().strip())
            
        try:            
            descricao = soup.find_all('div',{'id':'desc'})
            for desc in descricao:
                registro.append(desc.getText())
        except:
            print('Erro ao adcionar os dados! 2')
        
        try:
            for classe in clases:
                table = pd.DataFrame()
                dados = []   
                
                if soup.find(id=classe):
                    table_html = soup.find(id=classe)
                    table = pd.read_html(str(table_html))[0]             
                    for i in table.columns:
                        #print(i)
                        time.sleep(3)
                        dados.append(str("||".join(table[i])))
                        #print(dados)
                    for k in range(0,len(dados)):
                        time.sleep(2)
                        #print(dados[k])
                        registro.append(dados[k])              
                else:
                    if classe == 'acaoInst':
                        for i in range(0,4):
                            registro.append('Nenhum registro encontrado')
                    elif classe == 'm':
                        for i in range(0,2):
                            registro.append('Nenhum registro encontrado')
        except:
            print('Erro ao adcionar os dados! 3')
        
        registro.append(url)
        result_dict = dict(zip(colunas,registro))
        time.sleep(3)
        
    else:
        print('Acesando os dados do link: {}, NÃO ESTÁ NO AR!'.format(url))
    df = df.append(result_dict, ignore_index=True)
df.to_csv("IPHAN_Imaterial.csv",encoding='utf-8-sig',index=False,sep=';')
