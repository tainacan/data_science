# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 11:53:34 2020
@author: robson
-----------------------------------------------------------------------------------------------
Objetivo do script:
    
O objetivo desse script é coletar os dados das páginas de patrimônio Arqueológico das regiões, foram
definidas a coleta por regiões e suas respectivas cidades e assim cirando a estrutura dos metadados.

Dificuldades:
    
Algumas cidades não tem fotos ou não estão dentro da estrutura da galeria de fotos, quando tem alguma foto
e não está na galeria a esrutura muda. 

-----------------------------------------------------------------------------------------------
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from lxml import html

colunas = ['região','cidade','cidade_título','cidade_descrição','cidade_imagens','cidade_descricao_imagens','cidade_link']
df = pd.DataFrame(columns=colunas)
dic_regiao = {'Norte': 874,'Nordeste': 875,'Centro-Oeste': 876,'Sudeste': 877,'Sul':878}

def limpaItem(item):
    item = str(item).replace("[", "")
    item = str(item).replace("]", "")
    item = str(item).replace("'", "")
    item = str(item).replace(u"\\xa0", "").strip()
    return item
def buscaDadosCidade(url,dados):
    site_cidades   = requests.get(url, verify=False)
    
    if site_cidades.status_code in range(200,300):
        soup_cidades    = bs(site_cidades.text, 'html.parser')
        tree_cidades    = html.fromstring(site_cidades.content)
        desc            = []
        desc_img        = []
        cidades_imagens = []
        cidades_dados   = []
        try:
            cidades_dados.append(soup_cidades.find('h2').getText())
        except:
            cidades_dados.append('')
        for i in range(1,len(soup.find_all('p',{'class':'AlignJustify'}))):
                desc.append(tree_cidades.xpath('//*[@id="master"]/article/div[3]/p[{}]/text()'.format(i)))
        desc = str(desc).replace("[", "")
        desc = str(desc).replace("]", "")
        desc = str(desc).replace("'", "")
        desc = str(desc).replace(u"\\xa0", "").strip()        
        cidades_dados.append(desc)        
        try:
                            
            for img in soup_cidades.find('div',{'class':'content-galeria content-galeria-fototeca'}).find_all('img'):
                cidades_imagens.append(str(img['src']))
                desc_img.append(img['data-content'])
            cidades_dados.append(str("||".join(cidades_imagens)))
            cidades_dados.append(str("||".join(desc_img)))
            
        except:
            try:
                cidades_dados.append(str('http://portal.iphan.gov.br'+soup_cidades.find('p',{'class':'AlignJustify'}).find('img')['src']))
                cidades_dados.append(soup_cidades.find('p',{'class':'AlignJustify'}).find('img')['title'])
            except:
                cidades_dados.append('')
                cidades_dados.append('')
        try:    
            cidades_dados.append(url)
        except:
            cidades_dados.append('')
    else:
        print('Site fora do ar!')        
    return cidades_dados

for desc_região, id_região in dic_regiao.items():
    
    url_base         = str("http://portal.iphan.gov.br/pagina/detalhes/{}/".format(id_região))
    site             = requests.get(url_base, verify=False)
    soup             = bs(site.text, 'html.parser')
    tree             = html.fromstring(site.content)
    dados            = []
    regiao_desc      = soup.find_all('p',{'class':'AlignJustify'})
       
    for i in range(1,len(soup.find('article').find_all('a')[4:])+1):
        result_dict     = {}
        dados           = []
        dados.append(desc_região)
        for desc_reg in range(0,len(soup.find_all('p',{'class':'AlignJustify'}))-2):
            dados.append(regiao_desc[desc_reg].getText())
        if ((desc_região == 'Nordeste') or (desc_região == 'Centro-Oeste')):
            dados.append(limpaItem(tree.xpath('//*[@id="master"]/article/div[3]/p[3]/a[{}]/text()'.format(i))))
            url = limpaItem(str(tree.xpath('//*[@id="master"]/article/div[3]/p[3]/a[{}]/@href'.format(i))))
            url = str('http://portal.iphan.gov.br'+url)
            cidades = buscaDadosCidade(url,dados)
            nova_lista = dados + cidades
            result_dict = dict(zip(colunas,nova_lista))
            
        else:
            dados.append(limpaItem(tree.xpath('//*[@id="master"]/article/div[3]/p[2]/a[{}]/text()'.format(i))))
            url = limpaItem(str(tree.xpath('//*[@id="master"]/article/div[3]/p[2]/a[{}]/@href'.format(i))))
            url = str('http://portal.iphan.gov.br'+url)
            cidades = buscaDadosCidade(url,dados)
            nova_lista = dados + cidades            
            result_dict = dict(zip(colunas,nova_lista))            
        df = df.append(result_dict, ignore_index=True)
df.to_csv("IPHAN_regiões_patrimônio_arqueológico.csv",encoding='utf-8-sig',index=False,sep=';')
    