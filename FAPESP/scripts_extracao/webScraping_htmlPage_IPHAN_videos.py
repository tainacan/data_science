# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 16:33:11 2020

@author: robson
"""

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
import requests as req


#ufs  = ['ac','al','am','ap','ba','ce','df','es','go','ma','mg','ms','mt','pa','pb','pe','pi','pr','rj','rn','ro','rr','rs','sc','se','sp','to']
ufs = ['ac','al']
driver = webdriver.Chrome(
    executable_path=r'C:\Users\wapRo\Documents\FAPESP\scripts\lib\chromedriver.exe')
imagens_lista = []

registros = []
items_df = pd.DataFrame()
colunas_videos = ['UF','LINK_PAGINA','TÍTULOS','LEGENDAS','URL']

def coletaDadosIframe(link_iframe):
    
    #print(link_iframe.text)
    time.sleep(2)
    soup = bs(driver.page_source, 'html.parser')
    #div = soup.find_all('div',{'class':'fototeca-col'})
    
    #iframe = req.get(link_iframe)
    html_iframe = bs(link_iframe.text, "html.parser")    
    try:        
        result_dict[colunas_videos[0]] = str(uf).upper()
        result_dict[colunas_videos[1]] = html_iframe.find('a')['href']
        result_dict[colunas_videos[2]] = html_iframe.find('title').getText().replace('- YouTube','').strip().upper()
        result_dict[colunas_videos[3]] = soup.find('p').getText().strip()
        result_dict[colunas_videos[4]] = url
        print(result_dict)       
        
    except:
        print('erro')

for uf in ufs:
    url = str('http://portal.iphan.gov.br/{}/videos'.format(uf))
    time.sleep(2)
    driver.get(url)
    result_dict = {}
    
    soup = bs(driver.page_source, 'html.parser')
    #div = soup.find_all('div',{'class':'fototeca-col'})   
    iframe = req.get(soup.find('iframe')['src'].replace('//','https://'))
    
    coletaDadosIframe(iframe)
    items_df = items_df.append(result_dict, ignore_index=True)
    
    #print(soup.find('iframe')['src'].replace('//','https://'))
    try:
    
        nregistros = int(soup.find('p',{'class':'nregistros'}).getText()[23:].strip())    
    
        if nregistros >= 1:
            links = soup.find_all('h4')
            for link in links:
                try:
                    xpath = str("//a[contains(text(),'{}')]".format(link.getText()))
                    time.sleep(3)
                    driver.find_element_by_xpath(xpath).click()
                    time.sleep(3)
                    html = bs(driver.page_source, 'html.parser')
                    iframe1 = req.get(html.find('iframe')['src'].replace('//','https://'))
                    coletaDadosIframe(iframe1)
                    items_df = items_df.append(result_dict, ignore_index=True)
            
                    print(html.find('iframe')['src'].replace('//','https://'))
                except:
                    continue
    except:
        continue
   

driver.quit()
items_df.T 

 
 