# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 22:17:34 2020

@author: robson
"""
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib3
urllib3.disable_warnings()

#Dados para requisição das páginas
url       = "https://sicg.iphan.gov.br/sicg/bem/visualizar/29427#&panel1-4"
url_popUP = 'https://sicg.iphan.gov.br/sicg/bens/29427/protecoes/5521/popUp'
site      = requests.get(url,verify=False)
popUp     = requests.get(url_popUP,verify=False)

soup      = bs(site.text, 'html.parser')
popUp     = bs(popUp.text,'html.parser')

#Definindo as variáveis com as tags HTML

colunas_label      = soup.find_all('label')
legend             = soup.find('div',{'id':'container_gestao'}).select('legend')
div_grupos         = soup.select('div#container_gestao div')
imagens            = soup.findAll('img')[10:]
fieldset_popUp_all = popUp.find('fieldset').find_all('legend')
span_all           = popUp.find_all('span')
li_all             = popUp.find('fieldset').find_all('li')

dicionario         = {}
columns            = []
registro           = []
contador           = 1

for lista_colunas in colunas_label:
    columns.append(lista_colunas.text.strip().replace(':',''))
    registro.append(re.sub(r'[\n\r]','',lista_colunas.find_next_sibling("div").getText().strip()))
    
#inicio dos dados do POPUP    
for i in range(1,len(span_all),2):
    columns.append(span_all[i].next_element.replace(':',''))
    
for i in range(2,len(span_all),2):
    registro.append(span_all[i].next_element.replace(':',''))
for i in range(1, len(fieldset_popUp_all)):
    columns.append(fieldset_popUp_all[i].next_element.strip().replace(':',''))
for i in range(0,2):
    registro.append('')
for i in range(0,len(li_all)):
    registro.append(li_all[i].getText().split())
columns.append(soup.find('div').b.next_element.strip())
registro.append(soup.find('div').b.next_element.next_element.strip())

# fim dos dados de popUp

#inicio dos dados de gestão do bem
for i in range(0,len(legend)):
    columns.append(legend[i].getText().strip())
for i in range(2,len(div_grupos)):
    registro.append(div_grupos[i].getText().strip())
for imagem in imagens:
    nome_columns = 'imagem ' + str(contador)
    link = 'https://sicg.iphan.gov.br'+imagem['src']   
    columns.append(nome_columns)
    registro.append(link)
    contador = contador + 1

#Fim dos dados de gestão do bem

#adicionando os dados em um dicionario     
dicionario= dict(zip(columns,registro)) 

#criando e exportando o DataFrame Pandas
df = pd.DataFrame.from_dict(dicionario,orient='index').T
df.to_csv("Relatorio_material.csv",encoding='utf-8-sig',index=False,sep=';')


