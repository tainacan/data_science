from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
import time

videos_iphan = pd.DataFrame(columns = ["Titutlo", "Link", "Página"])
n = 1

for i in range(18):
    
    print("Coletando vídeos da página {}".format(n))
    
    page = req.get('http://portal.iphan.gov.br/videos?pagina={}'.format(n))
    soup = bs(page.text, 'html.parser')
    videos = soup.findAll("li", {"class": "lista-galeria-vertical2-titulo"})

    for video in videos[5:]: #Os primeiros 5 vídeos se repetem em todas as páginas
        titulo = video.text
        link = video.find("a").get("href")
        
        videos_iphan = videos_iphan.append({"Titutlo":titulo, "Link":link, "Pagina":n}, ignore_index=True)
    n+=1
    time.sleep(5)
    
videos_iphan.to_csv("iphan_videos_ext.csv", index=False)
