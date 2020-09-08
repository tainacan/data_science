# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 17:42:28 2020

@author: robson
"""

from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time


class AcervoSergioBrito:
    def __init__(self, driver):
        self.driver = driver
        self.url = 'http://sbrittod.funarte.gov.br/sophia_acervo/'
        self.label = 'dados'
        self.items_df = pd.DataFrame()
        self.wait = WebDriverWait(self.driver, 60)

    def navega(self):
        self.driver.get(self.url)
        self.driver.switch_to.frame('mainFrame')

    def pesquisa(self, palavra_chave=' '):
        self.driver.find_element_by_id(self.label).send_keys(palavra_chave)
        self.driver.find_element_by_xpath('//input[@name="submit"]').click()
        try:
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(text(),'Hemeroteca')]")))
            self.driver.find_element_by_xpath(
                "//a[contains(text(),'Hemeroteca')]").click()
            time.sleep(2)

        except TimeoutException as ex:
            print("Erro ao fazer a pesquisa." + str(ex))
            self.driver.close()
            
    def paginacao(self):
        
        for i in range(0,4):
            
            if i == 0:
                
                print("pagina {}".format(i))
                time.sleep(3)
                self.buscaDados()
                
            elif i == 1:                
                time.sleep(5)
                pagina = str('//*[@id="ajxDiv"]/table[1]/tbody/tr[1]/td/a[1]')
                self.driver.find_element_by_xpath(pagina).click()
                print("Página {}".format(i))
                time.sleep(3)
                self.buscaDados()
            elif i == 2:
                time.sleep(5)
                pagina = str('//*[@id="ajxDiv"]/table[1]/tbody/tr[1]/td/a[4]')
                self.driver.find_element_by_xpath(pagina).click()
                print("Página {}".format(i))
                time.sleep(3)
                self.buscaDados()
            elif i == 3:
                time.sleep(5)
                pagina = str('//*[@id="ajxDiv"]/table[1]/tbody/tr[1]/td/a[5]')
                self.driver.find_element_by_xpath(pagina).click()
                print("Página {}".format(i))
                time.sleep(3)
                self.buscaDados()
                      

    def buscaDados(self):
        
        try:
            
            for i in range(2,27):#11,27
            
                result_dict = {}
                
                if i == 4:
                    link = str("//div[@id='divNewMain']//div[4]//table[1]//tbody[1]//tr[1]//td[4]//a[1]")
                    
                else:
                    link = str("//div[{}]//table[1]//tbody[1]//tr[1]//td[4]//a[1]".format(i))
                self.wait.until(EC.visibility_of_all_elements_located(
                    (By.XPATH, link)))
                
                self.driver.find_element_by_xpath(link).click()
                
                time.sleep(5)
                
                elemento = self.driver.find_element_by_xpath('//div[@id="ajxDiv"]//table[2]')
                
                html = bs(elemento.get_attribute('innerHTML'), 'html.parser')
                tds_colunas = html.find_all('td',{'class':'td_campo'})
                tds_valores = html.find_all('td',{'class':'td_valor'})
                
                for colunas in range(0,len(tds_colunas)):
                    #print(tds_colunas[colunas].getText())
                    print(tds_valores[colunas].getText())
                    
                    result_dict[tds_colunas[colunas].getText()] = tds_valores[colunas].getText()
                self.items_df = self.items_df.append(result_dict, ignore_index=True)
                
                time.sleep(4)
                self.driver.find_element_by_xpath("//a[contains(text(),'Resultado')]").click()
                
            
        except TimeoutException as ex:
            print("Erro ao buscar os dados. " + str(ex))
            self.driver.close()
            
    
gc = webdriver.Chrome(
    executable_path=r'C:\Users\wapRo\Documents\FAPESP\scripts\Acervo_Sergio_brito\chromedriver.exe')

acervo = AcervoSergioBrito(gc)
acervo.navega()
acervo.pesquisa('par')
acervo.paginacao()
df = acervo.items_df
df.to_csv("acervoSergioBrito.csv",encoding='utf-8-sig',index=False,sep=';')
acervo.driver.quit()
