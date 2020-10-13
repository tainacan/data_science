# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 21:53:10 2020

@author: robson
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
import urllib3
urllib3.disable_warnings()

#Definindo variáveis
colunas          = ['Nome', 'Condição', 'Tipo', 'UF', 'Município','Coordenada(s)_geográfica(s)','Contatos','Bens_vinculados_Condição','Bens_vinculados_Nome','Bens_vinculados_Categoria',
                    'Bens_vinculados_Abrangência','Ações_vinculados_Tipo','Ações_vinculados_Nome','Ações_vinculados_Instrumento','Ações_vinculados_Situação','Página']
url_base         = "https://sicg.iphan.gov.br/sicg/bemImaterial/instituicao/"
clases           = ['bemImaterial','acaoInst']
qtd_link         = 451 #quandtidade de sites que vão ser raspados 450
df               = pd.DataFrame(columns=colunas)


for links in range(1,qtd_link):
    
    url              = (url_base + "%s/" %(links))
    site             = requests.get(url, verify=False)
    soup             = bs(site.text, 'html.parser')
    colunas_label    = soup.find_all('label')
    result_dict      = {}
    registro         = []
    
    #Verifica se o link está no ar!
    if site.status_code in range(200,300):
        
        print('Acesando os dados do link:', format(url))
        
        for lista_colunas in colunas_label:        
            registro.append(lista_colunas.find_next_sibling("div").getText().strip())
        registro.append('Nenhum registro encontrado')
        try:
            for classe in clases:
                table = pd.DataFrame()
                dados = []
                
                if soup.find(id=classe):
                    table_html = soup.find(id=classe)
                    table = pd.read_html(str(table_html))[0]            
                    for i in table.columns:
                        dados.append(str("||".join(table[i])))
                        #print(dados)
                    for k in range(0,len(dados)):
                        time.sleep(2)
                        registro.append(dados[k])
                else:
                    if classe == 'bemImaterial':
                        for i in range(0,4):
                            registro.append('Nenhum registro encontrado')
                    else:
                        for i in range(0,4):
                            registro.append('Nenhum registro encontrado') 
                    
        except:
            registro.append('Nenhum registro encontrado')
        
        registro.append(url)
        result_dict = dict(zip(colunas,registro))
        time.sleep(3)
        
    else:
        print('Acesando os dados do link: {}, NÃO ESTÁ NO AR!'.format(url))
    df = df.append(result_dict, ignore_index=True)
df.to_csv("IPHAN_Instituição.csv",encoding='utf-8-sig',index=False,sep=';')