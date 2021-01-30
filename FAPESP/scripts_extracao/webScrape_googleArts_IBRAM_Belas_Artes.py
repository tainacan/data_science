import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

firefox = webdriver.Chrome()
wait = WebDriverWait(firefox, 60)
items_df = pd.DataFrame()
#%% Link das Coleções
link = "https://artsandculture.google.com"
page = requests.get("https://artsandculture.google.com/search/entity?p=museu-nacional-de-belas-artes")
soup = bs(page.content, 'html.parser')
colecoes = soup.find_all('li', class_='DuHQbc')
result_dict = {}

for colecao in colecoes:
    
    firefox.get(link + colecao.a['href'])
    time.sleep(2)
    #wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@class='os1Bab']")))
    firefox.find_elements_by_xpath("//*[@class='os1Bab']")[0].click()
    flag = True
    
    while flag == True:
        #wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='XD0Pkb']")))
        try:
            metadados = firefox.find_elements_by_xpath("//*[@class='XD0Pkb']")
            result_dict = {}
            result_dict['link_item'] = firefox.current_url
            result_dict['colecao'] = colecao.a['title']
            for metadado in metadados:
                if len(metadado.text.split(":")) == 2:
                    print(metadado.text)
                    result_dict[metadado.text.split(":")[0]] = metadado.text.split(":")[1].strip()
                    
                else:
                    
                    continue
                
            items_df = items_df.append(result_dict, ignore_index=True)
        except:
            continue
        
        try:
            wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@class='yzn9r fJnwRb']")))
            firefox.find_element_by_xpath("//*[@class='yzn9r fJnwRb']").click()
        except:
            flag = False
            
        time.sleep(5)
            
        print(flag)
        
#%%
items_df.to_csv('webScrape_GoogleArts_Belas_Artes.csv')
