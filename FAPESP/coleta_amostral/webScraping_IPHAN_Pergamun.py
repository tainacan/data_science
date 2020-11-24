# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 15:55:30 2020
@author: robson batista da silva
-----------------------------------------------------------------------------------------------
Objetivo do script:
    
O objetivo desse script é coletar os dados da página Pergamun do Iphan, para isso foram definidos
dois parâmetros como: a palavra chave de pesquisa “IPHAN” e filtrado pela as unidades da informação.
Caso queiram buscar outra palavra chave deve ser passado a nova palavra-chave no método pesquisa.

Dificuldades:
    
O sistema tem um tempo de resposta demorado.
Quando se clica em um item para fazer a raspagem dos dados, por algumas vezes o botão “fechar” 
não aparece causando assim a interrupção do script, pois a tela fica travada.
As unidades da informação que contêm  mais de mil itens não é possível acessa-los, devido a 
um bloqueio no sistema que limita a visalização de mil itens 

-----------------------------------------------------------------------------------------------

"""

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time
import re

class Pergamun:
    def __init__(self, driver):
        self.driver = driver
        self.url = 'https://pergamum.iphan.gov.br/biblioteca/index.php'
        self.texto_link = []
        self.label = 'termo_para_pesquisa'
        self.df = pd.DataFrame()
        self.wait = WebDriverWait(self.driver, 60)
    def navega(self):
        self.driver.get(self.url)
        time.sleep(5)
        
    def pesquisa(self, palavra_chave=' '):
        try:
            self.driver.find_element_by_id(self.label).send_keys(palavra_chave)
            locator = (By.CLASS_NAME,'pmu_btn11')
            self.wait.until(EC.element_to_be_clickable(locator))
            self.driver.find_element_by_id('pesq').click()
        except:
            self.driver.quit()
        
    def buscaUnidades(self):
        locator = (By.XPATH,'//*[@id="mais_chama_B"]/a')
        self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.find_element_by_xpath('//*[@id="mais_chama_B"]/a').click()
        
        locator = (By.XPATH,'//*[@id="div_filtro_pesq_bib"]/div')
        self.wait.until(EC.presence_of_element_located(locator))
        
        elemento = self.driver.find_element_by_xpath('//*[@id="div_filtro_pesq_bib"]/div')
        html = bs(elemento.get_attribute('innerHTML'), 'html.parser')
        div = html.find_all('div')
        for i in div:
            if (i.find('a',{'class':'link_cinza10'}).getText() != '+mais') and (i.find('a',{'class':'link_cinza10'}).getText() != 'CDP (Brasília)(1252)'):
                self.texto_link.append(i.find('a',{'class':'link_cinza10'}).getText().strip())
                
            
    def buscaDados(self):
        for texto in self.texto_link:
            try:
                self.driver.find_element_by_xpath('//*[@id="mais_chama_B"]/a').click()
            except:
                pass
            
            xpath = (str("//a[contains(text(),'{}')]").format(texto))
            locator = (By.XPATH,xpath)
            self.wait.until(EC.element_to_be_clickable(locator))
            
            self.driver.find_element_by_xpath(xpath).click()
            
            locator = (By.XPATH,'//*[@id="id_resultados_temp"]/div[1]/table/tbody/tr/td[3]/table/tbody/tr[1]/td/a')
            self.wait.until(EC.presence_of_element_located(locator))
            
            try:
                qtd_resultados = bs(self.driver.find_element_by_xpath('//*[@id="some_ebsco2"]/table/tbody/tr/td/div/span').get_attribute('innerHTML'), 'html.parser')
                total_pagina = qtd_resultados.find_all('a')[3:][0]['href']
                total_pagina = int(re.sub(r'[^0-9]','',total_pagina))
            except:
                total_pagina = 1
            print('A unidade {} tem {} páginas'.format(texto,total_pagina))
            contador = 0
            
            for k in range(0,total_pagina):
                print("O texto 3 {}".format(texto))
                for i in range(1,21):#21
                    time.sleep(3)           
                    result_dict = {}
                    registros = []
                    colunas = []
        
                    try:                        
            
                        xpath = str('//*[@id="id_resultados_temp"]/div[{}]/table/tbody/tr/td[3]/table/tbody/tr[1]/td/a'.format(i))
                        locator = (By.XPATH,xpath)
                        self.wait.until(EC.element_to_be_clickable(locator))                     
                       
                        self.driver.find_element_by_xpath(xpath).click()                    
                        
                        locator = (By.XPATH,'//*[@id="div_detalhes_acervo"]/div')
                        self.wait.until(EC.presence_of_element_located(locator))    
                        
                        elemento = self.driver.find_element_by_xpath('//*[@id="div_detalhes_acervo"]/div')
                        html = bs(elemento.get_attribute('innerHTML'), 'html.parser')
                        strong = html.find_all('strong')
                        for i in strong:
                            colunas.append(i.getText())
                        colunas.append('Unidade_de_Informação')
                        td = html.find_all('td')
                        for i in range(1,len(td),2):
                            registros.append(td[i].getText().strip())
        
                        registros.append(texto)
                        result_dict = dict(zip(colunas,registros))
        
                        self.df = self.df.append(result_dict, ignore_index=True)
        
                        time.sleep(2)
                        
                        self.driver.find_element_by_xpath("//div[@id='dados']//div[@id='fechar_2']").click()
                        contador = contador + 1
                        print(contador)
                    except:
                        time.sleep(2)
                        print("O texto 4 {}".format(texto))
                        print("caiu na exessão")
                        #time.sleep(2)
                        break
                #time.sleep(3)
                self.driver.find_element_by_xpath('//*[@id="id_paginas_temp"]/table/tbody/tr/td/span/a[3]').click()
                time.sleep(3)
            
            time.sleep(3)
    
        
firefox = webdriver.Firefox(
    executable_path=r'C:\Users\wapRo\Documents\FAPESP\scripts\lib\geckodriver.exe')        

iphanPergamun = Pergamun(firefox)
iphanPergamun.navega()

iphanPergamun.pesquisa('IPHAN')
iphanPergamun.buscaUnidades()
iphanPergamun.buscaDados()
df = iphanPergamun.df
df.to_csv("IPHAN_pergamun.csv",encoding='utf-8-sig',index=False,sep=';')
#%%
# A estrutura abaixo foi utilizada pois o script acima demora muita para coletar
# os dados e várias vezes houve estouro da memória causando o interrompendo do script,
#mas das vezes que o script parrou o dataframe salvou os dados até aquele momento. 

pergamun1 = pd.read_csv('C:/Users/wapRo/Documents/FAPESP/scripts/IPHAN/IPHAN_pergamun.csv',sep=';')
pergamun2 = pd.read_csv('C:/Users/wapRo/Documents/FAPESP/scripts/IPHAN/IPHAN_pergamun2.csv',sep=';')
pergamun3 = pd.read_csv('C:/Users/wapRo/Documents/FAPESP/scripts/IPHAN/IPHAN_pergamun3.csv',sep=';')
pergamun4 = pd.read_csv('C:/Users/wapRo/Documents/FAPESP/scripts/IPHAN/IPHAN_pergamun4.csv',sep=';')
pergamun5 = pd.read_csv('C:/Users/wapRo/Documents/FAPESP/scripts/IPHAN/IPHAN_pergamun5.csv',sep=';')
pergamun6 = pd.read_csv('C:/Users/wapRo/Documents/FAPESP/scripts/IPHAN/IPHAN_pergamun6.csv',sep=';')
pergamun6 = pergamun6[pergamun6['Unidade_de_Informação'] != 'IPHAN-SP(579)']


pergamun6 = pergamun6[pergamun6['Unidade_de_Informação'] != 'IPHAN-SP(579)']
pergamun5 = pergamun5[pergamun5['Unidade_de_Informação'] != 'IPHAN-SC(408)']
pergamun4 = pergamun4[pergamun4['Unidade_de_Informação'] != 'IPHAN-GO(548)']
pergamun =  pd.concat([pergamun1,pergamun2,pergamun3,pergamun4,pergamun5,pergamun6],axis=0)
print(pergamun['Unidade_de_Informação'].value_counts())

pergamun.to_csv("IPHAN_pergamun.csv",encoding='utf-8-sig',index=False,sep=';')

