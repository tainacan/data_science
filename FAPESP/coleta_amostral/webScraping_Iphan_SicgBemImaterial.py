import pandas as pd
import time
import random
import requests as req
from bs4 import BeautifulSoup as bs
import urllib3
urllib3.disable_warnings()
resultado = pd.DataFrame()
notFind = []

for i in range(101):
    n = random.randint(1,629)
    time.sleep(2)
    
    if i == 0:
        continue
    else:
        resultDict = {}
        
        try:
            url = 'https://sicg.iphan.gov.br/sicg/bemImaterial/rel/{}/'.format(n)
            page = req.get(url,verify=False)
            time.sleep(3)
            soup = bs(page.text, 'html.parser')
            descricao = soup.find_all("div", {"id": "desc"})[0].getText().strip()
            resultDict['descrição'] = descricao
            
        except:
            resultDict['descrição'] = ""
        
        try:
            acao_df = pd.read_html(url)
        except:
            time.sleep(10)
            try:
                acao_df = pd.read_html(url)
            except:
                notFind.append(n)
                continue
            
        resultDict['link'] = url
        print("Coletando o item {}-{}".format(n, i))
        
        for table in acao_df[0][0]:
            values = table.replace(":  ", ": ").split("  ")[1:]
                
            for value in values:
                try:
                    resultDict[value.split(":")[0].strip()] = value.split(":")[1].strip()
                except:
                    continue
#%%
    resultado = resultado.append(resultDict, ignore_index=True)
#%%
resultado.to_csv("iphan_SICG_bemImaterial.csv", index=False)
