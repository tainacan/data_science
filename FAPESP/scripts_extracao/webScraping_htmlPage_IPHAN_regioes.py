# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 15:53:16 2020
@author: Robson Batista da Silva

-----------------------------------------------------------------------------------------------
Objetivo do script:
    
O objetivo desse script é coletar os dados das páginas de patrimônio Material do Iphan, para isso foram
definidas a coleta por regiões e suas respectivas cidades e assim cirando a estrutura dos metadados.

-----------------------------------------------------------------------------------------------
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
from lxml import html

#Buscando os dados das regiões

range_regiao = [98,99,100,101,102]
colunas = ['região','região_descrição','região_link_imagem','região_link','cidade','cidade_descrição','cidade_link_imagens','cidade_descricao_imagens','cidade_link']
df = pd.DataFrame(columns=colunas)

for regioes in range_regiao:
    
    url_base         = str("http://portal.iphan.gov.br/pagina/detalhes/{}/".format(regioes))
    site             = requests.get(url_base, verify=False)
    soup             = bs(site.text, 'html.parser')
    tree             = html.fromstring(site.content)   
    dados            = []
    descricao        = []
    
    dados.append(soup.find_all('h2')[0].getText())
    
    print('---------------------')
    print(url_base)
    print(soup.find_all('h2')[0].getText())

    for i in range(2,len(soup.find_all('p',{'class':'AlignJustify'}))):
        descricao.append(tree.xpath('//*[@id="master"]/article/div[3]/p[{}]/text()'.format(i)))
    descricao = str(descricao).replace("[", "")
    descricao = str(descricao).replace("]", "")
    descricao = str(descricao).replace("'", "")
    descricao = str(descricao).replace(u"\\xa0", "").strip()
    dados.append(descricao)
    
    for img in soup.find('p').find_all('img'):
        imagem = str('http://portal.iphan.gov.br/'+img['src'])
    dados.append(imagem)
    dados.append(url_base)
    if soup.find_all('h2')[0].getText() == 'Sul':
        total_cidades = soup.find_all('p')[2:3]
    else:
        total_cidades = soup.find_all('p')[3:4]
    
    #Salvando os links que pertence a cada região
    for cidades in total_cidades:
        
    
        for link in range(0,len(cidades.find_all('a'))):
            site_cidades   = requests.get("http://portal.iphan.gov.br"+cidades.find_all('a')[link]['href'], verify=False)
            result_dict    = {}
            dados_cidade   = []
            time.sleep(2)
            soup_cidades   = bs(site_cidades.text, 'html.parser')
            
            #print(soup_cidades.find('h2'))
            #str("http://portal.iphan.gov.br"+t.find_all('a')[link]['href'])
            #links_cidades.append(str("http://portal.iphan.gov.br"+t.find_all('a')[link]['href']))
            links_cidades = str("http://portal.iphan.gov.br"+cidades.find_all('a')[link]['href'])
            
            #coleta os dados dos estados        
                       
            site_cidades   = requests.get(links_cidades, verify=False)
             #Verifica se o link está no ar!
            if site_cidades.status_code in range(200,300):
                
                print('Acesando os dados do link:', format(links_cidades))
                
                soup_cidades   = bs(site_cidades.text, 'html.parser')
                tree_cidades   = html.fromstring(site_cidades.content)
    
                desc = []
                imagens_cidades = []
                desc_img = []
    
                dados_cidade.append(soup_cidades.find('h2').getText())
                print(soup_cidades.find('h2').getText())
    
                for i in range(1,len(soup.find_all('p',{'class':'AlignJustify'}))):
                    desc.append(tree_cidades.xpath('//*[@id="master"]/article/div[3]/p[{}]/text()'.format(i)))
                desc = str(desc).replace("[", "")
                desc = str(desc).replace("]", "")
                desc = str(desc).replace("'", "")
                desc = str(desc).replace(u"\\xa0", "").strip()
                dados_cidade.append(desc)
                
                try:
                    for img in soup_cidades.find('div',{'class':'content-galeria content-galeria-fototeca'}).find_all('img'):
                        imagens_cidades.append(str(img['src']))
                        desc_img.append(img['data-content'])
                    dados_cidade.append(str("||".join(imagens_cidades)))
                    dados_cidade.append(str("||".join(desc_img)))
                except:
                    dados_cidade.append('')
                    dados_cidade.append('')
                    
                dados_cidade.append(links_cidades)
                nova_lista = dados + dados_cidade
    
                result_dict = dict(zip(colunas,nova_lista))
                #print('-------------------------------')
                #print(result_dict['cidade'])
            else:
                print('Site fora do ar!')
            df = df.append(result_dict, ignore_index=True)   
    
df.to_csv("IPHAN_regiões.csv",encoding='utf-8-sig',index=False,sep=';')    