# -*- coding: utf-8 -*-

#%% Importa a base em xml e faz a leitura.
import xml.etree.ElementTree as ET
import pandas as pd
tree = ET.parse('03 - base_tombo_museu.txt') #Nome do documento xml, deve estar na mesma pasta do script.
root = tree.getroot()

lista_tags = []
dict_base = {}

#%%Ler os elementos da base

#Pega todas as tags/colunas do txt e coloca em uma lista.
for element in root:
    for tag in element:
        lista_tags.append(tag.tag)
lista_tags = set(lista_tags) #Tira a repetição das tags/colunas

#Cria listas para cada tag em um dicionário.
for tag in lista_tags:
    dict_base[tag] = []

print(dict_base.keys())

#%% Processo de Conversão
lista_multiplos=[]

#Lê os valores das tags/colunas do txt e armazena nas respectivas lista no dicionário.
for i in range(len(root)):
    for tag in dict_base.keys():

        if root[i].find(tag) != None:
            if len(root[i].findall(tag)) > 1:
                lista_teste.append(tag)
                for campo in root[i].findall(tag):
                    lista_multiplos.append(campo.text)
                dict_base[tag].append(";".join(lista_multiplos))
                lista_multiplos=[]

            elif len(root[i].findall(tag)) == 1:
                if root[i].find(tag).find('a') == None:
                    for campo in root[i].findall(tag):
                        dict_base[tag].append(campo.text)
                elif root[i].find(tag).find('a') != None:
                    dict_base[tag].append(str(root[i].find(tag).find('a').attrib['href'])+';'+str(root[i].find(tag).find('a').text))

        elif root[i].find(tag) == None:
            dict_base[tag].append('Nulo')


#%%Exportação
#Transforma o dicionário em um DataFrame para ser exportado para csv
base_csv = pd.DataFrame(dict_base)
base_csv.to_csv('base_resultante.csv', encoding='utf-8')
