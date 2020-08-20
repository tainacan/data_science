# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 12:14:19 2020

@author: robson
"""
import re
import requests
import pandas as pd
import time
import urllib3
from bs4 import BeautifulSoup as bs
urllib3.disable_warnings()



colunas          = ['Nome','Tipo','Instrumento','Situação','Data início','Data fim','UF','Município','Coordenada(s) geográfica(s)', 'Quantidade de imagens','Quantidade de videos',
                   'Quantidade de audios','Início da análise final','Início da análise preliminar','Início da instrução técnica','Conclusão da análise final','Conclusão da análise preliminar',
                   'Conclusão da instrução técnica','Descrição','Página']
url_base         = "https://sicg.iphan.gov.br/sicg/bemImaterial/acao/"
registro         = []
qtd_link         = 98 #quantidades de links que vão ser raspados
df               = pd.DataFrame(columns=colunas)


for links in range(1,qtd_link):
    
    url              = (url_base + "%s/" %(links))
    site             = requests.get(url, verify=False)
    soup             = bs(site.text, 'html.parser')
    colunas_label    = soup.find_all('label')[:18]
    
    #Verifica se o link está no ar!
    if site.status_code in range(200,300):
        
        print('Acesando os dados do link:', format(url))
        
        for lista_colunas in colunas_label:        
            registro.append(lista_colunas.find_next_sibling("div").getText().strip())
            
        registro.append(soup.find('div',{'id':'descricao'}).getText().strip())
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