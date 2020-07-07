#Pensar em coletar primeiro uma amostra de metadados, 
#para verificar se há diferença entre os documentos na exposição de metadados

from bs4 import BeautifulSoup as bs
import requests as req

page = req.get('http://acervo.bn.gov.br/sophia_web/acervo/detalhe/1')
soup = bs(page.text, 'html.parser')

##### Metadados

#Metadados Principais
metadata_ = soup.find_all("label", {"class":"control-label"}) #iterar pelos resultados - metadados

#Metadados de Vocabulário Controlado
metadata_vocab = soup.find_all("label", {"class":"display-block"}) # Iterar pelos resultados - metadados de vocabulários controlados

#Metadados de Exemplar
metadata_exemp = soup.find_all("th", {"class":"hidden-xs hidden-sm"}) # Iterar pelos resultados - metadados de exemplares

##### Valores

#Valores de Título e Subtítulo
title = soup.find_all("h1", {"class": "titulo"})[0].getText().strip() #Não iterar, valores repetidos
subtitle = soup.find_all("a", {"class": "subtitulo"})[0].getText().strip() #Não iterar, valores repetidos

#Valores dos Metadados Principais
value_ = soup.find_all("p")[:-1] #o último valor não é referente à um metadado, iterar sob os resultados - valores dos metadados

#Valores dos termos dos metadados dos vocabulários controlados (para assuntos)
value_assunto = soup.find_all("span", {"itemprop":"about"})
value_assunto[0].getText().strip() #iterar dentro desses dados

#Valores dos termos dos metadados dos vocabulários controlados (para autores)
value_autor = soup.find_all("span", {"itemprop":"name"})
value_autor[0].getText().strip() #iterar dentro desses dados

#Valores para os metadados do exemplar
value_exemp = soup.find_all("td", {"class":"hidden-xs hidden-sm"})
value_exemp[0].getText().strip() #iterar dentro desses dados
