import pandas as pd
import time
import random
import requests as req
from bs4 import BeautifulSoup as bs
import urllib3
urllib3.disable_warnings()
from collections import defaultdict

resultado = pd.DataFrame()
notFind = []
#%%
n = 1
url = 'https://sicg.iphan.gov.br/sicg/bem/visualizar/{}'.format(n)
page = req.get(url,verify=False)
soup = bs(page.text, 'html.parser')
campos = soup.find_all("fieldset")

#%%
for i in range(100):
    time.sleep(3)
    n = random.randint(1, 28900)
    print("Coletando o item {}".format(n))
    url = 'https://sicg.iphan.gov.br/sicg/bem/visualizar/{}'.format(n)
    
    page = req.get(url,verify=False)
    soup = bs(page.text, 'html.parser')
    campos = soup.find_all("fieldset")
    
    colectDict = defaultdict(list)
    resultDict = {}
    
    for i in range(len(campos)):
        for j in range(len(campos[i].find_all("label"))):
            colectDict[campos[i].find_all("label")[j].text.split(":")[0]].append( campos[i].find_all("div")[j].text.strip())
    
    for key in colectDict.keys():
        resultDict[key] = "||".join(colectDict[key])

    resultDict['link'] = url
    
    resultado = resultado.append(resultDict, ignore_index=True)

resultado.to_csv("iphan_SICG_bemMaterial.csv", index=False)
