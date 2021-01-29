import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import pandas as pd

items_df = pd.DataFrame()
#%% Link das Coleções
page = requests.get("https://mnba.gov.br/portal/colecoes.html")
soup = bs(page.content, 'html.parser')
colecoes = soup.find_all('div', class_='sprocket-mosaic-image-container')

for colecao in colecoes:
    link_colecao = "https://mnba.gov.br"+colecao.a['href']
    nome_colecao = colecao.a.img['alt']
    colecao_page = requests.get("https://mnba.gov.br"+colecao.a['href'])
    colecao_soup = bs(colecao_page.content, 'html.parser')
    objetos = colecao_soup.find_all('div', class_='sprocket-features-container')
    
    print("Coletando objetos da coleção {}".format(nome_colecao))
    
    for objeto in objetos:
        collection_dict = {}
        titulo = objeto.find('div', class_='sprocket-features-content').h2.a.text
        link_item = "https://mnba.gov.br"+objeto.find('div', class_='sprocket-features-content').h2.a['href']
        descricao = objeto.find('div', class_='sprocket-features-desc').span.text
        link_img = "https://mnba.gov.br"+objeto.find('div', class_='sprocket-features-img-container').a.img['src']
        
        collection_dict['colecao'] = nome_colecao
        collection_dict['link_colecao'] = link_colecao
        collection_dict['titulo'] = titulo
        collection_dict['link_item'] = link_item
        collection_dict['descrição'] = descricao
        collection_dict['link_imagem'] = link_img
        print("Objeto {} coletado.".format(titulo))
        
        items_df = items_df.append(collection_dict, ignore_index=True)    
        time.sleep(2)
        
    time.sleep(10)
#%%
items_df.to_csv("MuseuBelasArtes_.csv")
