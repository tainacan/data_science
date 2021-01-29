import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
page = requests.get("http://museuscastromaya.com.br/colecoes/")
soup = bs(page.content, 'html.parser')

items_df = pd.DataFrame()
#%% Coleta dos nomes e links das coleções
colecoes = soup.find_all('a', class_='wrapper-colecao')
for colecao in colecoes:
    nome_colecao = colecao.text
    link_colecao = colecao['href']
    # Coleta dos metadados e links das imagens
    page = requests.get(link_colecao)
    soup = bs(page.content, 'html.parser')
    objetos = soup.find_all('div', class_='gallery-overlay-image-wrapper')
    print("Coletando objetos da coleção {}".format(nome_colecao))
    
    for objeto in objetos:
        collection_dict = {}
        link_img = objeto.figure.img['src']
        desc_img = objeto.figure.figcaption.text
        collection_dict['colecao'] = nome_colecao
        collection_dict['link_colecao'] = link_colecao
        collection_dict['link_imagem'] = link_img
        collection_dict['descrição'] = desc_img
        print("Objeto {} coletado.".format(link_img))    
        items_df = items_df.append(collection_dict, ignore_index=True)        
    time.sleep(3)
    
items_df.to_csv("museucastromaya_GoogleArts.csv")
