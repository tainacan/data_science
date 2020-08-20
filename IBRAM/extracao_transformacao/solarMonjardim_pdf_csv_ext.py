# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 17:29:21 2020

@author: luisr
"""

#Bblioteca para extraçao do texto do PDF.
import PyPDF2
#Biblioteca para extrair padrões de texto.
import re
#Biblioteca para listar ps múltiplos PDFs.
import glob
#Biblioteca para criar e salvar os dados no CSV.
import csv
import pandas as pd

resultado = pd.DataFrame()
#%%
path = ""

#Abre o PDF
pdfFileObj= open(path,'rb')
#Lê o PDF
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#Pega o Número de Páginas
n_pages = pdfReader.getNumPages()

for page in range(n_pages):
    
    if page < 39:
        continue
    else:
        
        #print('Extraindo Texto da Página {}/{}'.format(page,n_pages))

        #Pega a página do PDF
        pageObj = pdfReader.getPage(page)

        #Extrai o texto da página do PDF
        text = pageObj.extractText()
        
        if page > 99:
            print(text)
            content_list = text[3:].split("\n")
            content_list = filter(None, content_list)
            content = "||".join(content_list)
            pagina = text[:3]
                        
        else:
            content_list = text[2:].split("\n")
            content_list = filter(None, content_list)
            content = "||".join(content_list)
            pagina = text[:2]
            
        
        resultado = resultado.append({'pagina':pagina, 'conteudo':content}, ignore_index=True)
        #print('Texto extraído da página {}'.format(page))
#%%
resultado = resultado.to_csv("", index = False)
