# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
import requests as req
import random
import time
import pandas as pd
not_find = []
result_df = pd.DataFrame(columns = ['Link', 'Código', 'Título', 'Subtítulo', 'Resumo', 'Idioma', 'ISBN', 'Descrição física', 'Nota de fonte de aquisição',
                                    'Nota de dissertação ou tese', 'Notas locais 6', 'Outros títulos', 'Notas locais 7',
                                    'Série', 'Nota de citação/referência', 'Notas locais 5', 'Notas locais 9',
                                    'Localização', 'Material', 'Nota de histórico de procedência',
                                    'Classificação Dewey', 'Título uniforme', 'Forma do registro', 'Título especial',
                                    'Periodicidade', 'Nota de forma física adicional', 'Número de chamada', 'Publicação',
                                    'Nota de idioma', 'Nota de reprodução', 'Nota geral', 'Título uniforme coletivo',
                                    'Notas locais', 'Notas locais 8', 'Nota bibliográfica', 'Edição', 'Notas locais 1',
                                    'Sites', 'ISSN', 'Assuntos', 'Autoria'])

for obj_id in range(100):
    
    result_dict = {}
    autor_list = []
    assunto_list = []
    
    n = random.randint(1,1748689)
    
    print("\nAcessando os metadados do item {}".format(n))
    
    link = 'http://acervo.bn.gov.br/sophia_web/acervo/detalhe/{}'.format(n)
    page = req.get(link)
    soup = bs(page.text, 'html.parser')
    
    result_dict['Link'] = link
    result_dict['Código'] = n
    
    print("   * Coletando Título/Subtítulo")
    #Valores de Título e Subtítulo
    try:
        result_dict['Título'] = soup.find_all("h1", {"class": "titulo"})[0].getText().strip() #Não iterar, valores repetidos
    except:
        print("   * Item {} não existe".format(n))
        not_find.append(n)
        
        continue
    try:
        result_dict['Subtítulo'] = soup.find_all("a", {"class": "subtitulo"})[0].getText().strip() #Não iterar, valores repetidos, verificar se exite primeiro
    except:
        result_dict['Subtítulo'] = ''
    
    print("   * Coletando os metadados principais")
    #Metadados Principais
    metadata_ = soup.find_all("label", {"class":"control-label"}) #iterar pelos resultados - metadados
    
    value_ = soup.find_all("p")[:-1] #o último valor não é referente à um metadado, iterar sob os resultados - valores dos metadados
    
    for i in range(len(metadata_)):
        result_dict[metadata_[i].text] = value_[i].text
        
    #Metadados de Vocabulário Controlado
    metadata_vocab = soup.find_all("label", {"class":"display-block"}) # Iterar pelos resultados - metadados de vocabulários controlados
    
    #Valores dos termos dos metadados dos vocabulários controlados (para assuntos)
    value_assunto = soup.find_all("span", {"itemprop":"about"})
    
    #Valores dos termos dos metadados dos vocabulários controlados (para autores), verificar se existe
    value_autor = soup.find_all("span", {"itemprop":"name"})
    
    print("   * Coletando os metadados de Autoria e Assuntos")
    #Valores de Autor
    if not value_autor:
        print("    * Sem valor de autor")
        value_autor = ""
        
    else:
        for autor_term in value_autor:
            autor_list.append(autor_term.getText().strip())
        value_autor = "||".join(autor_list)
    
    
    #Valores de Assunto
    if not value_assunto:
        print("    * Sem valor de assunto")
        value_assunto = ""
        
    else:
        for assunto_term in value_assunto:
            assunto_list.append(assunto_term.getText().strip())
        value_assunto = "||".join(assunto_list)
    
    
    result_dict["Autoria"] = value_autor
    result_dict["Assuntos"] = value_assunto
    
    for column in result_df.columns:
        if column not in result_dict.keys():
            result_dict[column] = ""
    
    result_df = result_df.append(result_dict, ignore_index=True)

    print("   * Metadados para o item {} coletados.".format(n))
    time.sleep(7)

result_df.to_csv("bn_acervo.csv", index=False)
