# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 10:37:23 2020

@author: luisr
"""
from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
import time
import cssutils

result_df = pd.DataFrame(columns=['link', 'pagina'])

for page in range(43):
    
    if page == 0:
        
        app_page = req.get('https://www.flickr.com/photos/culturanegra/')
        soup = bs(app_page.text, 'html.parser')
        photos = soup.findAll("div", {"class": "view photo-list-photo-view requiredToShowOnServer photostream awake"})
        
        for photo in photos:
            
            style = cssutils.parseStyle(photo.get('style'))
            url = style['background-image']
            url = url.replace('url(', '').replace(')',"")
            
            result_df = result_df.append({'link':url,'pagina':page}, ignore_index=True)
            
    else:
        
        app_page = req.get('https://www.flickr.com/photos/culturanegra/page{}'.format(page))
        soup = bs(app_page.text, 'html.parser')
        photos = soup.findAll("div", {"class": "view photo-list-photo-view requiredToShowOnServer photostream awake"})
        
        for photo in photos:
            
            style = cssutils.parseStyle(photo.get('style'))
            url = style['background-image']
            url = url.replace('url(', '').replace(')',"")
            
            result_df = result_df.append({'link':url,'pagina':page}, ignore_index=True)
            
    print("Objetos da página {} coletados, experando 5 segundos para a próxima página".format(page))
    
    time.sleep(10)

result_df.to_csv("C://Users//luisr//OneDrive//Documentos//palmares_flickr_photos.csv")
