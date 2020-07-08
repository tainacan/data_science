from docx.api import Document
from collections import defaultdict
import win32com.client as win32
from unidecode import unidecode
from time import sleep #define um periodo de tempo entre uma ação e outra
from tqdm import tqdm #adiciona uma barra de "loading"
import glob
import csv
import os
import pandas as pd

#Mapear os metadados para extração dos dados do texto das fichas
metadata_dict = {"Report":"","Familia":"","Especie":"","Procedencia":"","Codigo":"","Registro no":"","Camadas de Crescimento":"",
                 "Vasos":"","Observacoes":"","Parenquima axial":"","Estrutura estratificada":"","Raios":"",
                 "Traqueides e fibras":"","Inclusoes minerais":"","Referencias bibliograficas":"","Dados ecologicos":"",
                 "Gaveta":"","Procedencia":"","Limites":"",
                 "Porosidade":"","Arranjo":"","Agrupamento":"","Diametro tangencial medio":"",
                 "Numero medio de vasos por mm2":"","Tiloses":"","Observacoes":"","Placas de perfuracao":"",
                 "Pontoacoes intervasculares":"","Pontoacoes guarnecidas":"","Pontoacoes raio-vasculares":"",
                 "Parenquima paratraqueal":"","Seriacao":"","Numero medio de raios por mm":"","Tamanho":"",
                 "Caracteristicas especiais":"","Composicao celular":"","Floema incluso":"",
                 "Cristais prismaticos":"","Outros cristais":"","Caracteristicas diagnosticas":"",
                 "Fibras":"","Pontoacoes das fibras":"","Espessura da parede das fibras":"",
                 "Canais intercelulares":""}

#O script coleta o texto de cada documento docx e separa os termos do texto pelo espaço, colocando os termos em uma lista.

#Os metadados mapeados são buscados pelos índices da lista de termos obtida. O valor dos metadados é obtido ao delimitar o 
#conjunto de termos entre um metadado encontrado e o próximo.

result_dict = defaultdict(list)

for file in glob.glob(''):
    
    word = win32.Dispatch('Word.Application')
    word.Visible = 0
    
    document = Document(file)
    doc = word.Documents.Open(file)
    
    print("r"+ file.split("\\")[-1].strip(".docx").strip(".rtf"), end=",")
    
    paragraph_list = []
    for paragraph in doc.paragraphs:

        sentence = str(paragraph).rstrip('\r\x07').replace("\t\t"," ").strip("\t")
        words = sentence.split(":")

        for word in words:

            word=unidecode(word)

            if "\t\x0b" in word:
                unicode_words = word.splitlines()

                for unicode_word in unicode_words:

                    if unicode_word != '':
                        paragraph_list.append(unicode_word.strip())

            elif "\x0b" in word:
                unicode_words = word.splitlines()

                for unicode_word in unicode_words:

                    if unicode_word != '':
                        paragraph_list.append(unicode_word.strip())
            else:
                if word != '':
                    paragraph_list.append(word.strip())
    
    values_dict = defaultdict(list)

    for key in metadata_dict.keys():

        for value_i1 in paragraph_list:

            if unidecode(value_i1) == key:

                i_1 = paragraph_list.index(value_i1)
                key_1 = key

                for value_i2 in paragraph_list[i_1+1:]:

                    if value_i2 in metadata_dict.keys():

                        i_2 = paragraph_list[i_1:].index(value_i2)
                        break

                values_dict[key_1].append(" ".join(paragraph_list[i_1+1:i_1+i_2]))
    
    values_dict['Report'].append("r"+ file.split("\\")[-1].strip(".docx").strip(".rtf"))
    
    for metadata in metadata_dict.keys():

        if metadata in values_dict.keys():
            result_dict[metadata].append("||".join(list(set(values_dict[metadata]))))
        else:
            result_dict[metadata].append("")
    doc.Close()
    sleep(2.5)
    
result_df = pd.DataFrame.from_dict(result_dict)
result_df.to_csv('', index=False)
