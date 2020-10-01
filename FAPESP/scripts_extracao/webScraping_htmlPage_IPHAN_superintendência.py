# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
import requests as req
import time

class IPHAN:
    def __init__(self, driver):
        self.driver   = driver
        self.ufs      = ['ac','al','am','ap','ba','ce','df','es','go','ma','mg','ms','mt','pa','pb','pe','pi','pr','rj','rn','ro','rr','rs','sc','se','sp','to']     
        #self.ufs = ['ac']
        self.registro = []
        self.colunas  = ['UF','LINK_PAGINA','TÍTULOS','IMAGENS','FOTÓGRAFOS']
        self.colunas_videos = ['UF','LINK_PAGINA','TÍTULOS','LEGENDAS','URL']
        self.items_df = pd.DataFrame()
        self.items_df_videos = pd.DataFrame()
        self.wait     = WebDriverWait(self.driver, 60)
        self.imagens_lista   = []
        self.fotografo_lista = []
        
    def navega(self):
        for self.uf in self.ufs:
            url = str('http://portal.iphan.gov.br/{}/galeria'.format(self.uf))
            time.sleep(2)
            self.driver.get(url)
            self.coletasDados()           
            
            try:
                pagina = bs(self.driver.page_source, 'html.parser')
                qtd_pagina = int(pagina.find_all('p',{'class':'nregistros'})[0].getText()[23:])
                ul = pagina.find_all('ul',{'class':'pagination'})
                for li in ul:
                    qtd_pagina = len(li.find_all('li'))
                #self.wait(EC.visibility_of_element_located(By.XPATH,"//a[contains(text(),'Próxima')]"))
                #self.driver.find_element_by_xpath('//*[@id="master"]/div[1]/div/div/div/ul/li[5]/a').click()
                time.sleep(2)
                for i in range(0,qtd_pagina):
                    time.sleep(2)
                    self.driver.find_element_by_xpath('//*[@id="master"]/div[1]/div/div/div/ul/li[5]/a').click()
                    
                    self.coletasDados()
            except:
                print("A Página {} não tem paginação".format(url))
    def coletasDados(self):
        
        self.soup = bs(self.driver.page_source, 'html.parser')
        self.div = self.soup.find_all('div',{'class':'fototeca-col'})
        
        time.sleep(3)
        
        for links in self.div:
            link = links.find_all('h3')[0].getText()
            link_pagina = links.find_all('a')[0]['href']
            xpath = str("//h3[contains(text(),'{}')]".format(link))
            
            time.sleep(3)
            self.driver.find_element_by_xpath(xpath).click()
            elemento = self.driver.page_source
            html = bs(elemento, 'html.parser',)  
            imgs = html.find_all('div',{'class':'content-galeria content-galeria-fototeca'})
            for img in imgs:
                result_dict = {}
                result_dict[self.colunas[0]] = str(self.uf).upper()
                result_dict[self.colunas[1]]  = link_pagina
                result_dict[self.colunas[2]] = html.find_all('h2')[0].getText().strip()
                imagem = img.find_all('img')
                
                for k in range(0,len(imagem)):
                    self.imagens_lista.append(imagem[k]['src'].strip())
                
                result_dict[self.colunas[3]] = str("||".join(self.imagens_lista))
                
                for y in range(0,len(imagem)):
                    try:
                        self.fotografo_lista.append(imagem[y]['title'].strip())
                    except:
                        self.fotografo_lista.append('')
                
        
                result_dict[self.colunas[4]] = str("||".join(self.fotografo_lista))
                
            self.items_df = self.items_df.append(result_dict, ignore_index=True)
            time.sleep(2)
            self.driver.execute_script("window.history.go(-1)")
            
    def coletaDadosIframe(self,link_iframe,uf,url):
    
        time.sleep(2)
        soup = bs(self.driver.page_source, 'html.parser')        
        html_iframe = bs(link_iframe.text, "html.parser")
        
        try:        
            self.result_dict[self.colunas_videos[0]] = str(uf).upper()
            self.result_dict[self.colunas_videos[1]] = html_iframe.find('a')['href']
            self.result_dict[self.colunas_videos[2]] = html_iframe.find('title').getText().replace('- YouTube','').strip().upper()
            self.result_dict[self.colunas_videos[3]] = soup.find('p').getText().strip()
            self.result_dict[self.colunas_videos[4]] = url
                  
            
        except:
            print('Erro ao inserir os dados no dicionário')
    def coletasDadosVideos(self):
        time.sleep(5)
        
        for uf in self.ufs:
            url = str('http://portal.iphan.gov.br/{}/videos'.format(uf))
            time.sleep(2)
            self.driver.get(url)
            self.result_dict = {}
            
            soup = bs(self.driver.page_source, 'html.parser')
            iframe = req.get(soup.find('iframe')['src'].replace('//','https://'))
            
            self.coletaDadosIframe(iframe,uf,url)
            self.items_df_videos = self.items_df_videos.append(self.result_dict, ignore_index=True)
            
            try:
            
                nregistros = int(soup.find('p',{'class':'nregistros'}).getText()[23:].strip())    
            
                if nregistros >= 1:
                    links = soup.find_all('h4')
                    for link in links:
                        try:
                            xpath = str("//a[contains(text(),'{}')]".format(link.getText()))
                            time.sleep(3)
                            self.driver.find_element_by_xpath(xpath).click()
                            time.sleep(3)
                            html = bs(self.driver.page_source, 'html.parser')
                            iframe = req.get(html.find('iframe')['src'].replace('//','https://'))
                            self.coletaDadosIframe(iframe,uf,url)
                            self.items_df_videos = self.items_df_videos.append(self.result_dict, ignore_index=True)
                    
                        except:
                            continue
            except:
                continue
        
        
gc = webdriver.Chrome(
    executable_path=r'C:\Users\wapRo\Documents\FAPESP\scripts\lib\chromedriver.exe')

galeria = IPHAN(gc)
galeria.navega()
df = galeria.items_df
df.to_csv("IPHAN_galerias.csv",encoding='utf-8-sig',index=False,sep=';')
galeria.driver.quit()

videos = IPHAN(gc)
videos.coletasDadosVideos()
df_videos = videos.items_df_videos
videos.driver.quit()
df_videos.to_csv("IPHAN_videos.csv",encoding='utf-8-sig',index=False,sep=';')
          
            
