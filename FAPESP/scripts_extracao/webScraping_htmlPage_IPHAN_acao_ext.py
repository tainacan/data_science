# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 12:14:19 2020
DIFICULDADES ENCONTRADAS:
01 - Quando o fieldset não tem registro, não é possível pegar o nome da class que apareceria
caso tivesse, sendo assim tive que procurar nos demias links um registro que tivesse registro no fildset e
adicionar algumas condições para esse ocasião.
02- algumas classes não possuí um nome intuitivo, ou seja existe classes com nomes por exemplo: M 

 
 
  
@author: robson
"""

import requests
import pandas as pd
import time
import urllib3
from bs4 import BeautifulSoup as bs
urllib3.disable_warnings()


#Definindo variáveis
colunas          = ['Nome','Tipo','Instrumento','Situação','Data início','Data fim','UF','Município','Coordenada(s) geográfica(s)', 'Quantidade de imagens','Quantidade de videos',
                   'Quantidade de audios','Início da análise final','Início da análise preliminar','Início da instrução técnica','Conclusão da análise final','Conclusão da análise preliminar',
                   'Conclusão da instrução técnica','Descrição','Localização_específica','Atividades_Tipo','Atividades_Nome','Bens_vinculados_Condição','Bens_vinculados_Nome',
                    'Bens_vinculados_Categoria','Bens_vinculados_Abrangência','Instituições_Partícipes_Condição','Instituições_Partícipes_Nome','Instituições_Partícipes_Tipo',
                    'Documentos_vinculados','Abrangência_UF','Abrangência_Municípios','Palavras-chave:','Links','Página']
url_base         = "https://sicg.iphan.gov.br/sicg/bemImaterial/acao/"
registro         = []
clases           = ['ativ','bemImaterial','inst','doc','m']
qtd_link         = 326 #quandtidade de sites que vão ser raspados
df               = pd.DataFrame(columns=colunas)


for links in range(1,qtd_link):

    url              = (url_base + "%s/" %(links))
    site             = requests.get(url, verify=False)
    soup             = bs(site.text, 'html.parser')
    colunas_label    = soup.find_all('label')[:18]
    result_dict      = {}
    registro         = []
    
    #Verifica se o link está no ar!
    if site.status_code in range(200,300):
        
        print('Acesando os dados do link:', format(url))
        
        for lista_colunas in colunas_label:        
            registro.append(lista_colunas.find_next_sibling("div").getText().strip())
            
        registro.append(soup.find('div',{'id':'descricao'}).getText().strip())
        registro.append(soup.find('div',{'id':'local'}).getText().strip())
        
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
                elif classe == 'doc':
                    registro.append('Nenhum registro encontrado')
                    
                else:
                    
                    if classe == 'ativ':
                        for i in range(0,2):
                            registro.append('Nenhum registro encontrado')
                    elif classe == 'bemImaterial':
                        for i in range(0,4):
                            registro.append('Nenhum registro encontrado')
                    elif classe == 'inst':
                        for i in range(0,3):
                            registro.append('Nenhum registro encontrado')
                    elif classe == 'm':
                        for i in range(0,2):
                            registro.append('Nenhum registro encontrado')
                    else:
                        registro.append('Nenhum registro encontrado')                      
                               
                                
        except:
            print("Erro ao adicionar os dados") 
        
        try:       

            registro.append(soup.find(id='palchav').getText().strip())
            registro.append(soup.find(id='links').getText().strip())
        except:
            for i in range(0,2):
                registro.append('Nenhum registro encontrado')
                print("Erro ao adicionar os dados")            
        
        registro.append(url)
        result_dict = dict(zip(colunas,registro))
        
    else:
        print('Acesando os dados do link: {}, NÃO ESTÁ NO AR!'.format(url))
    df = df.append(result_dict, ignore_index=True)
   
df.to_csv("IPHAN_Ação.csv",encoding='utf-8-sig',index=False,sep=';')

