# coding: utf-8
###INTRODUÇÃO###
"""
O script abaixo foi realizado para realizar testes de escala no Tainacan, 
como produto este script gera bases de dados com valores controlados de 
acordo com os parâmetros inseridos na variável ranges (vetor que corresponde
à quantidade de bases e à quantidade de linhas de cada base) e na variável
metadataDict (dicionário com os parametros de divisão dos valores para cada metadado)
"""

#%%Bibliotecas Importadas
import pandas as pd
from collections import defaultdict
import datetime
from dateutil.relativedelta import *

###PARÂMETROS###
"""
O dicionário metadataDict aponta os metadados como chaves, e como valores
a quantidade de valores distintos previstos para cada metadado. 

O processo ocorre através da divisão do número de linhas da base a ser gerada pelo valor
correspondente do metadados mencionado no dicionário metadataDict, o que vai gerar
para cada metadado um número controlado de valores diferentes.

Já os tipos de valores  para cada metadado são definidos na etapa de geração das bases,
de acordo com o termo inserido nas chaves do dicionário metadataDcit.
"""

#%%
#Parametros de tamanho das 6 bases geradas (quantidade de linhas)
"""
Foram pensados 16 metadadados, sendo 12 deles do tipo valor textual, 
um do tipo data, um do típo numérico, um metadado fazendo alusão à valores
de título e mais um metadados fazendo alusão à valores de descrição. Se assemelhando à
proposta do padrão de metadados DC, que menciona ao menos 15 metadaos principais para
descrição de objetos digitais
"""

#Elementos = Quantidade de Bases / Valores = Número de Linhas
ranges = [10000,20000,50000,100000,200000,500000]

#Dicionário de metadados gerados
#Chaves = Metadados / Valores = Divisor da base de dados.
metadataDict = {"m1":2, "m2":5, "m3":10, "m4":20, "m5":50, "m6":100, "m7":200,
               "m8":500, "m9":1000, "m10": 2000,"datas":2000, "numeros":2000,
               "m11":5000, "m12":10000, "title":"", "description":""}

###Base de valores textuais###
"""
Para produzir valores textuais para os metadados m1 a m12 foi utilizada uma
base com os nomes de cidades americanas que apresenta 19.490 termos diferentes.
munDf = pd.read_csv('uscities.csv')
"""

#Parágrafo de exemplo a ser replicado na base
paragrafo = "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\
Phasellus in risus lorem. Nullam eget leo maximus, eleifend ligula in,\n \
vehicula neque. Nullam porta massa eu ligula interdum vulputate. Donec\
sed justo vel sapien rutrum faucibus at a dolor. Nunc at ligula id urna\
egestas maximus. Sed vitae dui at lacus fermentum pretium ac ac mauris.\n \
Quisque fringilla, massa fermentum molestie ultricies, felis nisl lobortis\
libero, vel fermentum sapien felis ac sem. Suspendisse iaculis lorem felis,\
vitae faucibus ex ultrices non."

#%%Gerador das bases
for total in ranges:
    print(total)
    resultDict = defaultdict(list)

    for key in metadataDict.keys():
        cont_values = 0
        print(key, metadataDict[key])
       
        #para o título cria um conjunto de caracteres alfanumérico com um prefixo "xyz" + um iterador + sufixo "ABC"
        if key == "title":
            for txtValue in range(total):
                resultDict[key].append("xyz"+str(txtValue)+"ABC")
                
        #Para metadado de descrição replica o parágfrafo de exepmlo de acordo com a quantidade de itens
        elif key == "description":
            for parag in range(total):
                resultDict[key].append(paragrafo)
                
        #Para datas adiciona datas de acordo com os parametros da base gerada.
        elif key == "datas":
            for data in range(metadataDict[key]):
                for dataPlus in range(int(total/metadataDict[key])):
                    d = datetime.date.today() - datetime.timedelta(days=cont_values)
                    resultDict[key].append(d)
                cont_values+=1
        #Para o metadado numérico gera valores iterados de acordo com os parâmetros da base gerada.
        elif key == "numeros":
            for numeros in range(metadataDict[key]):
                for numero in range(int(total/metadataDict[key])):
                    resultDict[key].append(cont_values)
                cont_values+=1
        #Para os demais metadados, utiliza uma base com nomes de cidades dos EUA, e de acordo com o iterador,
        #foi selecionada a posição do vertor correspondente ao nome de uma cidade
        else:
            for i in range(metadataDict[key]):
                for j in range(int(total/metadataDict[key])):
                        resultDict[key].append(munDf['city'][cont_values])
                cont_values+=1
    
    resultDf = pd.DataFrame.from_dict(resultDict)
    resultDf.index.names = ['Identificador']
    resultDf.to_csv("{}_generateDb(full).csv".format(total))
