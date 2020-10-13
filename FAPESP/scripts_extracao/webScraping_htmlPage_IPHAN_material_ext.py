# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 22:17:34 2020

@author: robson
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
import urllib3
urllib3.disable_warnings()

#Definindo variáveis
colunas          = ['Recorte_territorial', 'Recorte_temático', 'Identificação_do_universo', 'UF', 'Município', 'CEP', 'Coordenada(s)_geográfica(s)', 
                    'Endereço','Nome', 'Nome_popular', 'Natureza', 'Tipo', 'Estado_de_Conservação', 'Estado_de_Preservação', 'Uso_do_Solo',
                    'Entorno_do_bem', 'Síntese','Síntese_histórica', 'Meios_de_acesso_ao_bem', 'Outras_Informações','Investimento',
                    'Fiscalização_Autorização','Códigos_vinculados','Outras_localidades_vinculadas','Contato','Documentos',
                    'links_imagens','data-description_imagens','tilte_imagens','Página']
url_base         = "https://sicg.iphan.gov.br/sicg/bem/visualizar/"
clases           = ['con','doc']
qtd_link         = 2999 #quandtidade de sites que vão ser raspados 101 2999
df               = pd.DataFrame(columns=colunas)

for links in range(1,qtd_link):
    
    url              = (url_base + "%s" %(links))
    site             = requests.get(url, verify=False)
    soup             = bs(site.text, 'html.parser')
    colunas_label    = soup.find_all('label')[:20]
    result_dict      = {}
    registro         = []
    
    #Verifica se o link está no ar!
    if site.status_code in range(200,300):
        
        print('Acesando os dados do link:', format(url))
        
        for lista_colunas in colunas_label:        
            registro.append(lista_colunas.find_next_sibling("div").getText().strip())
            
        #registro.append(soup.find('div',{'id':'desc'}).getText().strip())
        try:
            div_grupos         = soup.select('div#container_gestao div')
            for i in range(2,len(div_grupos)):
                registro.append(div_grupos[i].getText().strip())
        except:
            print("Erro ao acessar os dados! 1")
        try:
            div_imagens = soup.find_all('div',{'class':'container_multimidiaClosed'})
            for i in div_imagens:
                imagens = i.find_all('img')
                link = []
                data_description = []
                title = []            
                for imagem in imagens:   
                    link.append(str('https://sicg.iphan.gov.br'+imagem['src']))
                    data_description.append(imagem['data-description'])
                    title.append(imagem['title'])
                registro.append(str("||".join(link)))
                registro.append(str("||".join(data_description)))
                registro.append(str("||".join(title))) 
        except:
            print("Erro ao acessar os dados! 2 ")
        
        registro.append(url)
        result_dict = dict(zip(colunas,registro))
        time.sleep(3)
        
    else:
        print('Acesando os dados do link: {}, NÃO ESTÁ NO AR!'.format(url))
    df = df.append(result_dict, ignore_index=True)
df.dropna(inplace=True)
df.to_csv("IPHAN_material.csv",encoding='utf-8-sig',index=False,sep=';')


