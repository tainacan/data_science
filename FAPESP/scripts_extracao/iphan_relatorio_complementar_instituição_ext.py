# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 21:53:10 2020

@author: robson
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib3
urllib3.disable_warnings()

#definindo variáveis
url = "https://sicg.iphan.gov.br/sicg/bemImaterial/instituicao/450/"
site = requests.get(url,verify=False)
soup = bs(site.text, 'html.parser')

colunas_label = soup.find_all('span',{'class':'grid10'})
qtd_label = len(soup.find_all('legend')) 
td = [soup.find('tr',class_='odd').text.strip().split('\n'),soup.find('tr',class_='even').text.strip().split('\n')]
dicionario = {}
call = []
registro = []


for lista_colunas in colunas_label:
    call.append(lista_colunas.label.text.replace(':','').strip())
    registro.append(lista_colunas.div.getText().strip())
for i in range(3,qtd_label):
    if soup.find_all('legend')[i].next_element == 'Ações vinculadas':
        call.append(soup.find_all('legend')[i].next_element)
        registro.append(td)        
    else:
        call.append(soup.find_all('legend')[i].next_element)
        registro.append(soup.find('span',{'class':'grid12'}).next_sibling.strip())
    dicionario= dict(zip(call,registro))  
dicionario
df = pd.DataFrame.from_dict(dicionario,orient='index').T
df.to_csv("Relatório_complementar_Instituição.csv",encoding='utf-8-sig',index=False,sep=';')
df.head()