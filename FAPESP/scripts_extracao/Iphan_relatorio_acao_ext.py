# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 11:02:37 2020

@author: robson
"""

import re
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib3
urllib3.disable_warnings()

url = "https://sicg.iphan.gov.br/sicg/bemImaterial/acao/85/"
site = requests.get(url,verify=False)

soup = bs(site.text, 'html.parser')

colunas_label = soup.find_all('label')
qtd_label = len(soup.find_all('fieldset',{'class':'clean'}))
th = soup.find('table',{'id': 'ativ'}).next_element.next_sibling.text.strip().split('\n')
td = soup.find('tr',class_='odd').text.strip().split('\n')
dicionario = {}
calunas = []
registro = []
contador = 0

for lista_colunas in colunas_label:
    #Dentro desse array exite duas tags label que não tem descrição. o contador entrar nessas posição e busca o campo fieldset
    if contador == 18:        
        for k in range(1,qtd_label):
            if (k == 1 or k == 2):
                calunas.append(soup.find_all('fieldset',{'class':'clean'})[k].legend.text.strip())
                registro.append(re.sub(r'[\n\r]','',soup.find_all('fieldset',{'class':'clean'})[k].div.text.strip()))
                
            elif (soup.find_all('fieldset',{'class':'clean'})[k].legend.text.strip() == "Atividades"):
                for th_td in range(len(th)): 
                    #Acresentando ao nome da coluna _atividade, para não haver conflito com outras colunas que tem o mesmo nome.
                    calunas.append(th[th_td]+"_atividade")
                    registro.append(td[th_td])            
            else:
                calunas.append(soup.find_all('fieldset',{'class':'clean'})[k].legend.text.strip())
                registro.append(soup.find_all('fieldset',{'class':'clean'})[k].legend.next_element.next_element.strip())               
    else:
        #pula as tags label que estão em brancas
        if not lista_colunas.text.strip():
            pass
        else:
            #adicionando as tags label 
            calunas.append(lista_colunas.text.strip().replace(':',''))
            registro.append(lista_colunas.find_next_sibling("div").getText().strip())
            #criando um dicionario
            dicionario= dict(zip(calunas,registro))            
    contador = contador + 1
    
df = pd.DataFrame.from_dict(dicionario,orient='index').T
df.to_csv("Relatorio_complementar_ação.csv",index=False,sep=';')