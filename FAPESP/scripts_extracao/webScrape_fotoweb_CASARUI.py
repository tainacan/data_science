# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 10:24:03 2020

@author: luisr
"""
from selenium import webdriver
import pandas as pd
import time

#%%
#Configura o webdriver como Firefox
#Link para donwload do geckodriver do Firefox - https://github.com/mozilla/geckodriver/releases
#Necessita do geckodriver salvo em uma pasta identificada nas variáveis de ambiente PATH.
#(Sugiro salvar na pasta do Python ou do Anaconda)

firefox = webdriver.Firefox()
main_page = "http://iconografia.casaruibarbosa.gov.br/fotoweb/Default.fwx"

firefox.get(main_page)
ok_button = firefox.find_element_by_xpath("//*[@id='idFwSubmit']")
ok_button.click()

time.sleep(3)

grid_obj = firefox.find_element_by_xpath("//*[@class='Zoom']")
grid_obj.click()

time.sleep(3)

titulo = firefox.find_element_by_xpath("//*[@class='Label']").text
currentUrl = firefox.current_url;

table = firefox.find_element_by_xpath("//*[@class='PreviewInfo']/table").get_attribute('outerHTML')
table_df  = pd.read_html(table)

result_table = table_df[0].dropna().transpose()
result_table.columns = result_table.iloc[0].values
result_table = result_table.drop(result_table.index[0])

result_table['Titulo'] = titulo
result_table['Link'] = currentUrl


for i in range(100):
    try:
        next_obj = firefox.find_element_by_xpath("//*[@class='nextImageLink']")
        next_obj.click()
        
        titulo = firefox.find_element_by_xpath("//*[@class='Label']").text
        currentUrl = firefox.current_url;
        
        table = firefox.find_element_by_xpath("//*[@class='PreviewInfo']/table").get_attribute('outerHTML')
        df  = pd.read_html(table)
    
        result_table_T = df[0].dropna().transpose()
        result_table_T.columns = result_table_T.iloc[0].values
        result_table_T = result_table_T.drop(result_table_T.index[0])
        
        result_table_T['Titulo'] = titulo
        result_table_T['Link'] = currentUrl
        
        result_table = result_table.append(result_table_T)
        time.sleep(5)
        
    except:
        time.sleep(10)
        
        next_obj = firefox.find_element_by_xpath("//*[@class='nextImageLink']")
        next_obj.click()
        
        titulo = firefox.find_element_by_xpath("//*[@class='Label']").text
        currentUrl = firefox.current_url;
        
        table = firefox.find_element_by_xpath("//*[@class='PreviewInfo']/table").get_attribute('outerHTML')
        df  = pd.read_html(table)
    
        result_table_T = df[0].dropna().transpose()
        result_table_T.columns = result_table_T.iloc[0].values
        result_table_T = result_table_T.drop(result_table_T.index[0])
        
        result_table_T['Titulo'] = titulo
        result_table_T['Link'] = currentUrl
        
        result_table = result_table.append(result_table_T)
    
    
#%%
print(result_table.to_csv("C://Users//luisr//OneDrive//Documentos//rui_fotoweb_ext.csv", index = False))
