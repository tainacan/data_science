# -*- coding: utf-8 -*-
"""
Created on Wed May  6 21:18:41 2020
@author: luisr
"""
import requests
import time
from sqlalchemy import create_engine

#Acesso ao banco de dados. Substituir o usuário e a senha.
mysqlEngine = create_engine('mysql+pymysql://user:password@localhost:3306/tainacan_api')
dbConnection = mysqlEngine.connect()
#Função para normalizar os termos (remove espaços do inicio e do fim, e define somente a primeira letra como maiúscula)
def normalize(string):
    string = string.strip()
    return string.capitalize()

#Função para tentar os requests à API. (Se a conexão cair espera 3 minutos para tentar novamente, se a API bloquear, espera 3 minutos também)
def try_request(endpoint):
    time.sleep(4)
    tentativas = 0
    try:
        request = requests.get(endpoint)

        while str(request) != "<Response [200]>":

            if str(request) == '<Response [504]>':
                print("Sem permissão")
                continue
            else:
                print(endpoint)
                print("Erro na requisição, tentando novamente em 3 minutos")
                print(str(request))

                time.sleep(180)
                request = requests.get(endpoint)
                tentativas+=1

                if tentativas > 3:
                    print("Excedeu o limite de tentativas, passando ao próximo")
                    continue
    except:
        print("Erro na requisição, tentando novamente em 3 minutos")
        time.sleep(180)
        request = requests.get(endpoint)
        
    return request
  
#Função para limpar tabela do SQL com contraints na Foreing Key
def truncate_table(table_name):
    dbConnection.execute("SET FOREIGN_KEY_CHECKS = 0;")
    dbConnection.execute("TRUNCATE table {};".format(table_name))
    dbConnection.execute("SET FOREIGN_KEY_CHECKS = 1;")

#Função para limpar os valores dos dicionários de apoio
def clean_dict(dictionaire):
    
    for key in dictionaire.keys():
        
        if type(dictionaire[key]) == list:
            dictionaire[key] = []
            
        if type(dictionaire[key]) == str:
            dictionaire[key] = ''
            
    return dictionaire
  
#Função para transformar valores me lista para string separado por " - "
def list_str(lista):
    lista = filter(None, lista)
    result = (' - ').join(list(set(lista)))
    return result
