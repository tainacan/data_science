import pandas as pd
import requests
from bs4 import BeautifulSoup

colunas_ancine = ['Publicacao','Titulo', 'Link']
coluna_troca = ['Titulo']
coluna_link = ['Link']
tabelaAncine = pd.DataFrame(columns=colunas_ancine)
tabelaTitulo = pd.DataFrame(columns=coluna_troca)
tabelaLink = pd.DataFrame(columns=coluna_link)

url = 'https://www.ancine.gov.br/publicacoes'
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')
lista_coleta = soup.find_all('div', class_='content-body pagina-de-lista')

for lista_colunas in lista_coleta:
    lista = lista_colunas.find_all('h3')
    for lista_dados in lista:
        colunas = lista_dados.find_all('a')
        for lista_apresen in colunas:
            apresentacoes = lista_apresen.get("href")
            req_sites = requests.get("https://www.ancine.gov.br/"+apresentacoes)
            if apresentacoes == "publicacoes/apresentacoes":
                soup = BeautifulSoup(req_sites.content, 'html.parser')
                buscar_page = soup.find_all('div', class_='content-body')
                for busca in buscar_page:
                    coleta_pdf = busca.find_all('a')
                    for dados in coleta_pdf:
                        apresentacoes = "Apresentacoes"
                        titulo = dados.get("title")
                        link = dados.get("href")
                        tabelaAncine = tabelaAncine.append({'Publicacao': apresentacoes, 'Titulo': titulo, 'Link': link}, ignore_index=True)
                    
                buscar_page = soup.find_all('ul', class_='pager')
                for busca in buscar_page:
                    perpage = busca.find_all('li', class_='pager-item')
                    for page in perpage:
                        endpoint = page.find_all('a')
                        for end in endpoint:
                            endpoint_url = end.get("href")
                            req_url = requests.get("https://www.ancine.gov.br"+endpoint_url)
                            soup = BeautifulSoup(req_url.content, 'html.parser')
                            lista_coleta = soup.find_all('div', class_='content-body')
                            for lista in lista_coleta:
                                coleta = lista.find_all('a')
                                for dados in coleta:
                                    apresentacoes = "Apresentacoes"
                                    titulo_pdf = dados.get("title")
                                    link_pdf = dados.get("href")
                                    tabelaAncine = tabelaAncine.append({'Publicacao': apresentacoes, 'Titulo': titulo_pdf, 'Link': link_pdf}, ignore_index=True)
                                    
            if apresentacoes == "publicacoes/artigos":
                soup = BeautifulSoup(req_sites.content, 'html.parser')
                buscar_page = soup.find_all('div', class_='content-body')
                for busca in buscar_page:
                    coleta_pdf = busca.find_all('a')
                    for dados in coleta_pdf:
                        apresentacoes = "Artigo"
                        titulo = dados.get("title")
                        link = dados.get("href")
                        tabelaAncine = tabelaAncine.append({'Publicacao': apresentacoes, 'Titulo': titulo, 'Link': link}, ignore_index=True)
                        
                buscar_page = soup.find_all('ul', class_='pager')
                for busca in buscar_page:
                    perpage = busca.find_all('li', class_='pager-item')
                    for page in perpage:
                        endpoint = page.find_all('a')
                        for end in endpoint:
                            endpoint_url = end.get("href")
                            req_url = requests.get("https://www.ancine.gov.br"+endpoint_url)
                            soup = BeautifulSoup(req_url.content, 'html.parser')
                            lista_coleta = soup.find_all('div', class_='content-body')
                            for lista in lista_coleta:
                                coleta = lista.find_all('a')
                                for dados in coleta:
                                    apresentacoes = "Artigos"
                                    titulo_pdf = dados.get("title")
                                    link_pdf = dados.get("href")
                                    tabelaAncine = tabelaAncine.append({'Publicacao': apresentacoes, 'Titulo': titulo_pdf, 'Link': link_pdf}, ignore_index=True)
                                    
            if apresentacoes == "publicacoes/catalogo-cinemabrasil":
                soup = BeautifulSoup(req_sites.content, 'html.parser')
                buscar_page = soup.find_all('div', class_='content-body')
                for busca in buscar_page:
                    coleta_pdf = busca.find_all('a')
                    for dados in coleta_pdf:
                        apresentacoes = "Catalogo de Filmes"
                        titulo = dados.get("title")
                        link = dados.get("href")
                        tabelaAncine = tabelaAncine.append({'Publicacao': apresentacoes, 'Titulo': titulo, 'Link': link}, ignore_index=True)

            if apresentacoes == "publicacoes/folhetos":
                soup = BeautifulSoup(req_sites.content, 'html.parser')
                buscar_page = soup.find_all('div', class_='content-body')
                for busca in buscar_page:
                    soup = BeautifulSoup(req_sites.content, 'html.parser')
                buscar_page = soup.find_all('div', class_='content-body')
                for busca in buscar_page:
                    dados_titulo = busca.find_all('h3')
                    for busca_titulo in dados_titulo:
                        apresentacoes = "Folhetos"
                        titulo = busca_titulo.next_element
                        tabelaTitulo = tabelaTitulo.append({'Titulo': titulo}, ignore_index=True)
                    coleta_pdf = busca.find_all('a')
                    for dados in coleta_pdf:
                        link = dados.get("href")
                        tabelaLink = tabelaLink.append({'Link': link}, ignore_index=True)
                for i in range(0,10):
                    tabelaAncine = tabelaAncine.append({'Publicacao': apresentacoes,'Titulo' : tabelaTitulo['Titulo'][i],'Link' : tabelaLink['Link'][i]}, ignore_index=True)
                    
            if apresentacoes == "publicacoes/livros":
                soup = BeautifulSoup(req_sites.content, 'html.parser')
                buscar_page = soup.find_all('div', class_='content-body')
                for busca in buscar_page:
                    dados_titulo = busca.find_all('h3')
                    for busca_titulo in dados_titulo:
                        apresentacoes = "Livros"
                        titulo = busca_titulo.next_element
                        tabelaTitulo = tabelaTitulo.append({'Titulo': titulo}, ignore_index=True)   
                    coleta_pdf = busca.find_all('a')
                    for dados in coleta_pdf:
                        link = dados.get("href")
                        tabelaLink = tabelaLink.append({'Link': link}, ignore_index=True)
                for i in range(10,12):
                    tabelaAncine = tabelaAncine.append({'Publicacao': apresentacoes,'Titulo' : tabelaTitulo['Titulo'][i],'Link' : tabelaLink['Link'][i]}, ignore_index=True)
            
tabelaAncine.to_excel('ancine.xlsx')
