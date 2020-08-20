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
colunas          = ['Nome', 'Condição', 'Tipo', 'UF', 'Município','Coordenada(s) geográfica(s)','Página']
url_base         = "https://sicg.iphan.gov.br/sicg/bemImaterial/instituicao/"
registro         = []
qtd_link         = 101 #quantidades de sites que vão ser raspados
df               = pd.DataFrame(columns=colunas)


for links in range(1,qtd_link):
    
    url              = (url_base + "%s/" %(links))
    site             = requests.get(url, verify=False)
    soup             = bs(site.text, 'html.parser')
    colunas_label    = soup.find_all('label')
    
    #Verifica se o link está no ar!
    if site.status_code in range(200,300):
        
        print('Acesando os dados do link:', format(url))
        
        for lista_colunas in colunas_label:        
            registro.append(lista_colunas.find_next_sibling("div").getText().strip())
            
        registro.append(url)            
        time.sleep(3)
        
    else:
        print('Acesando os dados do link: {}, NÃO ESTÁ NO AR!'.format(url))

# Faz a divisão da quantidade de registro raspado pela quantidade de colunas definida
n                = int(len(registro) / len(colunas)) 
splited          = []
qtd_registro     = len(registro)
for slices in range(n):
    inicio = int(slices*qtd_registro/n)
    fim = int((slices+1)*qtd_registro/n)
    splited.append(registro[inicio:fim])
    
#gera o DataFrame    
for lista in range(0,n):
    df = df.append(pd.Series(splited[lista],index=df.columns),ignore_index=True)