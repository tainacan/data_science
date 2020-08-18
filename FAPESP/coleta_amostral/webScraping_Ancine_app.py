from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
import time

result_df = pd.DataFrame(columns=['titulo', 'descricao', 'document', 'pagina'])

for page in range(9):
    
    if page == 0:
        app_page = req.get('https://www.ancine.gov.br/publicacoes/apresentacoes')
        soup = bs(app_page.text, 'html.parser')
        presentations = soup.findAll("td", {"class": "views-field views-field-title"})

        for presentation in presentations:
            result_df = result_df.append({'titulo':presentation.find('a').get('title'),
                      'descricao':presentation.text.strip(),
                      'document':presentation.find('a').get('href'),
                      'pagina':page}, ignore_index = True)
    else:
        
        app_page = req.get('https://www.ancine.gov.br/publicacoes/apresentacoes?page={}'.format(page))
        soup = bs(app_page.text, 'html.parser')
        presentations = soup.findAll("td", {"class": "views-field views-field-title"})

        for presentation in presentations:
            result_df = result_df.append({'titulo':presentation.find('a').get('title'),
                      'descricao':presentation.text.strip(),
                      'document':presentation.find('a').get('href'),
                      'pagina':page}, ignore_index = True)
            
    print("Objetos da página {} coletados, experando 5 segundos para a próxima página".format(page))
    time.sleep(5)


result_df.to_csv("ancine_app.csv")
