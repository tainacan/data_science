from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

url = "http://acervodigital.iphan.gov.br/xmlui/discover"
driver =webdriver.Firefox()
driver.get(url)
resultado = pd.DataFrame()

for i in range(10):
    print("Coletando a página {}".format(i+1))
    html = driver.page_source
    
    soup = bs(html, 'html.parser')
    conjunto = soup.find_all("div", {'class':'jscroll-inner'})
    
    itens_impar = conjunto[i].find_all("li", {'class':'result-list ds-artifact-item clearfix odd'})
    itens_par = conjunto[i].find_all("li", {'class':'result-list ds-artifact-item clearfix even'})
    
    for item in itens_impar:
        resultDict = {}
        valores = []
        core_tL = item.find("h2", {"class":"result-info"})
        core_aD = item.find("p", {"class":"result-info"})
        metadados = item.find("div", {"class":"metadata-open"}).find_all('li')
        
        item_link = "http://acervodigital.iphan.gov.br" + core_tL.find("a", href=True)['href'] if core_tL.find("a", href=True)['href'] != None else ""
        titulo = core_tL.find("a").text if core_tL.find("a") != None else ""
        autor = core_aD.find("span", {'class':'author'}).text if core_aD.find("span", {'class':'author'}) != None else ""
        date = core_aD.find("span", {'class':'date'}).text if core_aD.find("span", {'class':'date'}) != None else ""
        descricao = item.find("p", {"class":"result-descript"}).text if item.find("p", {"class":"result-descript"}) != None else ""
        
        resultDict = {'link':item_link, 'titulo':titulo, 'descrição':descricao, 'autor':autor, 'data':date}
        
        for metadado in metadados:
            
            meta = metadado.find('span', {"class":"metadata-field-title"}).text
            
            if len(metadado.find_all('span', {"class":"metadata-item"})) > 1:
                for valor in metadado.find_all('span', {"class":"metadata-item"}):
                    valores.append(valor.text.strip())
                    valorJoin = "||".join(valores)
            else:
                valorJoin = metadado.find_all('span', {"class":"metadata-item"})[0].text
                
            resultDict[meta] = valorJoin
            
        resultado = resultado.append(resultDict, ignore_index=True)
        
    for item in itens_par:
        resultDict = {}
        valores = []
        core_tL = item.find("h2", {"class":"result-info"})
        core_aD = item.find("p", {"class":"result-info"})
        metadados = item.find("div", {"class":"metadata-open"}).find_all('li')
        
        item_link = "http://acervodigital.iphan.gov.br" + core_tL.find("a", href=True)['href'] if core_tL.find("a", href=True)['href'] != None else ""
        titulo = core_tL.find("a").text if core_tL.find("a") != None else ""
        autor = core_aD.find("span", {'class':'author'}).text if core_aD.find("span", {'class':'author'}) != None else ""
        date = core_aD.find("span", {'class':'date'}).text if core_aD.find("span", {'class':'date'}) != None else ""
        descricao = item.find("p", {"class":"result-descript"}).text if item.find("p", {"class":"result-descript"}) != None else ""
        
        resultDict = {'link':item_link, 'titulo':titulo, 'descrição':descricao, 'autor':autor, 'data':date}
        
        for metadado in metadados:
            
            meta = metadado.find('span', {"class":"metadata-field-title"}).text
            
            if len(metadado.find_all('span', {"class":"metadata-item"})) > 1:
                for valor in metadado.find_all('span', {"class":"metadata-item"}):
                    valores.append(valor.text.strip())
                    valorJoin = "||".join(valores)
            else:
                valorJoin = metadado.find_all('span', {"class":"metadata-item"})[0].text
                
            resultDict[meta] = valorJoin
            
        resultado = resultado.append(resultDict, ignore_index=True)
    
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)
    
driver.close()

resultado.to_csv("iphan_acervoDigital.csv", index=False)   


