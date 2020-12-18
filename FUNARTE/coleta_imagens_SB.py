from bs4 import BeautifulSoup as bs

from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

inputFile = ""

driver = webdriver.Firefox()
url = 'http://sbrittod.funarte.gov.br/sophia_acervo/'
items_df = pd.DataFrame()
wait = WebDriverWait(driver, 120)
driver.get(url)
driver.switch_to.frame('mainFrame')
itens_count = 0

inputDf = pd.read_excel("path_to_file_here".format(inputFile))

for inputTitle in range(len(inputDf['Título'])):
    i_title = inputTitle
    
    print(inputDf['Título'][inputTitle], inputDf['Código do item'][inputTitle])

    palavra_chave = '"'+inputDf['Título'][inputTitle]+'"'

    try:    
        #Palavra Chave Input
        wait.until(EC.presence_of_element_located((By.ID,'campo1')))
        driver.find_element_by_id("campo1").send_keys(palavra_chave)
        
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@name="submit"]')))
        driver.find_element_by_xpath('//input[@name="submit"]').click()
        
        #Secao
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'{}')]".format(categoryClickTerm))))
        driver.find_element_by_xpath("//a[contains(text(),'{}')]".format(categoryClickTerm)).click()
        print("Clicado em Hemeroteca")
            
        #Pages Number
        def checkPages():
            
            pageActualList = []
            
            #wait.until(EC.presence_of_element_located((By.XPATH,'//td[@style="text-align: center;"]')))
            for pageNumber in driver.find_elements_by_xpath('//td[@style="text-align: center;"]'):
                pageActualList.append(pageNumber.text)
            
            return pageActualList
        
        #time.sleep(5)
        pages = checkPages()
    
    except:

        print("Não foram encontrados resultados para a busca")
        time.sleep(5)
        voltarHome = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Home')]")))
        voltarHome.click()
        continue
    
    print(pages)
    
    if not pages:
        
        try:
            print("Procurando Detalhes...")
            #Item
            wait.until(EC.element_to_be_clickable((By.XPATH,'//a[@title="Detalhes..."]')))
            
        except:
            print("Não foi possível clicar no link do termo: sem resposta")
            time.sleep(5)
            voltarHome = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Home')]")))
            voltarHome.click()
            continue
        
        iLink = []
        
        #mapeia a quantidade de itens da página
        wait.until(EC.presence_of_element_located((By.XPATH,'//a[@title="Detalhes..."]')))
        for item_link in driver.find_elements_by_xpath('//a[@title="Detalhes..."]'):
            iLink.append(item_link.get_attribute('href'))
            
        #itera para cada item
        print("Contando Itens")
       
        for i in range(len(iLink)):
            itens_count+=1
            result_dict = {}
            
            result_dict["InputTitle"] = inputDf['Título'][inputTitle]
           
            #Itera entre os itens
            item_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="{}"]'.format(iLink[i]))))
            item_element.click()
            
            try:
                
                #Coleta link da imagem do item
                wait.until(EC.presence_of_element_located((By.XPATH,'//div[@id="ajxDiv"]/img[@id="img_item"]')))
                imgLink = driver.find_element_by_xpath('//div[@id="ajxDiv"]/img[@id="img_item"]').get_attribute('src')
                result_dict["Link"] = imgLink
                
            
                #Coletar Link para as Imagens
                wait.until(EC.presence_of_element_located((By.XPATH,'//td[@id="iNumImg"]/b')))
                imgsNumber = driver.find_elements_by_xpath('//td[@id="iNumImg"]/b')
        
                image_list = []
                for j in range(int(imgsNumber[1].text)):
        
                    #Clica no link da da Imagem
                    linksImgs = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#"]/img[@title = "Ampliar Imagem..."]')))
                    linksImgs.click()
                     
                    #Muda para a pop up que abriu da imagem
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(3)
                    #Pega o Link da Imagem
                    wait.until(EC.presence_of_element_located((By.XPATH,'//div[@id="divImg"]/img[@id="img"]')))
                    imgLink = driver.find_element_by_xpath('//div[@id="divImg"]/img[@id="img"]').get_attribute('src')
                    image_list.append(imgLink)
        
                    #Volta para a página do Item
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(3)
                    proxImgButton = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Próximo')]")))
                    proxImgButton.click()
            
                    special_doc = image_list[0]
                    if len(image_list) > 1:
                        special_att = "||".join(image_list[1:])
                    else:
                        special_att = ""
    
                result_dict["special_document"] = special_doc
                result_dict["special_attachments"] = special_att
                
            except:
                result_dict["Link"] = "Imagem não encontrada"
                result_dict["special_document"] = "Imagem não encontrada"
                result_dict["special_attachments"] = "Imagem não encontrada"
        
            
            items_df = items_df.append(result_dict, ignore_index=True)
            #Volta para a página de itens
            voltarResultado = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Resultado')]")))
            voltarResultado.click()
        
        time.sleep(5)
            
    else:
        
        page_count = 0
        while ">" in pages[0]:
            page_count+=1
            
            #Caso ocorra erro na coleta entre páginas deixar zero para coletas sem erros
            if page_count < 0:
                 pageElement = wait.until(EC.element_to_be_clickable((By.XPATH, '//td[@style="text-align: center;"]/a[contains(text(),">")]')))
                 pageElement.click()
                 print("pulando a página {}".format(page_count))
                 time.sleep(10)
                 
            else:
            
                print("Verificando a página {} de itens".format(page_count))
            
                try:
                    print("Procurando Detalhes... para mais de um item")
                    #Item
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//a[@title="Detalhes..."]')))
                    
                except:
                    time.sleep(5)
                    voltarHome = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Home')]")))
                    voltarHome.click()
                    print("Não foi possível clicar no link do termo: sem resposta")
                    continue
                
                iLink = []
                
                wait.until(EC.presence_of_element_located((By.XPATH,'//a[@title="Detalhes..."]')))
                for item_link in driver.find_elements_by_xpath('//a[@title="Detalhes..."]'):
                    iLink.append(item_link.get_attribute('href'))
                    
                for i in range(len(iLink)):
                    itens_count+=1
                    result_dict = {}
                    
                    result_dict["InputTitle"] = inputDf['Título'][inputTitle]
                   
                    #Itera entre os itens
                    item_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="{}"]'.format(iLink[i]))))
                    item_element.click()
                    
                    try:
                                               
                        #Coleta link da imagem do item
                        wait.until(EC.presence_of_element_located((By.XPATH,'//div[@id="ajxDiv"]/img[@id="img_item"]')))
                        imgLink = driver.find_element_by_xpath('//div[@id="ajxDiv"]/img[@id="img_item"]').get_attribute('src')
                        result_dict["Link"] = imgLink
                        
                    
                        #Coletar Link para as Imagens
                        wait.until(EC.presence_of_element_located((By.XPATH,'//td[@id="iNumImg"]/b')))
                        imgsNumber = driver.find_elements_by_xpath('//td[@id="iNumImg"]/b')
                
                        image_list = []
                        for j in range(int(imgsNumber[1].text)):
                
                            #Clica no link da da Imagem
                            linksImgs = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#"]/img[@title = "Ampliar Imagem..."]')))
                            linksImgs.click()
                             
                            #Muda para a pop up que abriu da imagem
                            driver.switch_to.window(driver.window_handles[1])
                            time.sleep(3)
                            #Pega o Link da Imagem
                            wait.until(EC.presence_of_element_located((By.XPATH,'//div[@id="divImg"]/img[@id="img"]')))
                            imgLink = driver.find_element_by_xpath('//div[@id="divImg"]/img[@id="img"]').get_attribute('src')
                            image_list.append(imgLink)
                
                            #Volta para a página do Item
                            driver.switch_to.window(driver.window_handles[0])
                            time.sleep(3)
                            proxImgButton = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Próximo')]")))
                            proxImgButton.click()
                    
                            special_doc = image_list[0]
                            if len(image_list) > 1:
                                special_att = "||".join(image_list[1:])
                            else:
                                special_att = ""
            
                        result_dict["special_document"] = special_doc
                        result_dict["special_attachments"] = special_att
                        
                    except:
                        result_dict["Link"] = "Imagem não encontrada"
                        result_dict["special_document"] = "Imagem não encontrada"
                        result_dict["special_attachments"] = "Imagem não encontrada"
                            
                        items_df = items_df.append(result_dict, ignore_index=True)
                    
                    if itens_count%5 == 0:
                        time.sleep(10)
                        
                    
                    #Volta para a página de itens
                    voltarResultado = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Resultado')]")))
                    voltarResultado.click()
        
                #time.sleep(5)
                pageElement = wait.until(EC.element_to_be_clickable((By.XPATH, '//td[@style="text-align: center;"]/a[contains(text(),">")]')))
                pageElement.click()
                
                pages = checkPages()
                #print(pages)
                time.sleep(5)
                
    time.sleep(5)
    voltarHome = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Home')]")))
    voltarHome.click()
    
    print("{} itens verificados".format(itens_count))
    print("{} titulos pesquisados".format(i_title+1))
#%%
outputFile = "v"

items_df.to_csv("{}".format(outputFile))
