import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

items_df = pd.DataFrame()
#%% Link das Coleções
link = 'https://mnba.gov.br'
page = requests.get("https://mnba.gov.br/portal/imprensa/galeria-de-videos.html")
soup = bs(page.content, 'html.parser')

paginas = soup.find_all('a', class_='pagenav')
objetos = soup.find_all('li', class_='span4')

for objeto in objetos:
    result_dict = {}
    link_item = link + objeto.a['href']
    titulo = objeto.find('div', class_='caption').h3.a.text
    result_dict['titulo'] = titulo
    result_dict['link_item'] = link_item
    items_df = items_df.append(result_dict, ignore_index=True)
    print("{} coletado.".format(titulo))
    
for pagina in paginas:
    
    #Checar somente páginas numéricas
    try:
        int(pagina.text)
        
        print("Coletando objetos da página {}".format(pagina.text))
    
        page = requests.get(link + pagina['href'])
        soup = bs(page.content, 'html.parser')
        objetos = soup.find_all('li', class_='span4')
        
        for objeto in objetos:
            result_dict = {}
            link_item = link + objeto.a['href']
            titulo = objeto.find('div', class_='caption').h3.a.text
            result_dict['titulo'] = titulo
            result_dict['link_item'] = link_item
            items_df = items_df.append(result_dict, ignore_index=True)
            print("{} coletado.".format(titulo))
    except:
        break        
        
    time.sleep(3)
    
items_df.to_csv('museuNacionalBelasAartes_Vídeos.csv')
