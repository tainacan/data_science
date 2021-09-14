import glob #Lista as pastas e arquivos
from docx.api import Document #Manipulação de Arquivos docx
import win32com.client as win32 #Manipulação de Arquivos docx
import csv
import time
import os
import pandas as pd

#Aciona a api do microsoft word
word = win32.gencache.EnsureDispatch('Word.Application')
word.Visible = 0

files = glob.glob("/Fichas/*.docx") #lista os arquivos com a extensão .docx


#Grava os dados de cada tabela da ficha em células em uma planilha CSV
with open("_v2.csv", "w", encoding='utf-8', newline='') as f:
    f_writer = csv.writer(f)
    
    for ficha in files:
            print("*****************************")
            print("Acessando a Ficha ", ficha)
            
            if "~$" in ficha: #Pula arquivos temporários do Word
                continue
                print("Pulando Arquivo Temporário")
                
            else:
                doc = word.Documents.Open(ficha) #Abre a ficha
                
                tables = doc.Tables #Encontra as tabelas da ficha
                
                values_list = []#Lista para armazenar os dados das tabelas encontradas
                values_list.append(ficha.split("/")[-1]) 
                
                for table in tables: #Looping para percorrer a matriz de dados das tabelas (Colunas e Linhas)
                    for column in range(len(table.Columns)):
                        for row in range(len(table.Rows)):
                            try:
                                values_list.append(table.Cell(Row = row+1, Column = column+1).Range.Text.rstrip('\r\x07'))#Adiciona os dados de cada tabela encontrada em uma lista
                            except:
                                #Exceção criada pois a numeração de identação da tabela ultrapassa o limite na busca após a última tabela
                                continue
                doc.Close(False)#Fecha a ficha em Word
                
                f_writer.writerow(values_list)#Salva uma linha de dados no CSV
