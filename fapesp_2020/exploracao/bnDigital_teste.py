#Extração de metadados do ponto de acesso http://acervo.bndigital.bn.br/sophia/index.html
#A previsão é que existam 101.818 itens
#As páginas de metadados são configuradas como HTML dentro de outro HMTL através de FRAMES, por isso usamos a biblioteca Selenium para navegar entre os frames e coletar os dados.

from selenium import webdriver
import pandas as pd

#Configura o webdriver como Firefox
#Link para donwload do geckodriver do Firefox - https://github.com/mozilla/geckodriver/releases
#Necessita do geckodriver salvo em uma pasta identificada nas variáveis de ambiente PATH.
#(Sugiro salvar na pasta do Python ou do Anaconda)
firefox = webdriver.Firefox()

#Abre a página da URL selecionada
firefox.get('http://acervo.bndigital.bn.br/sophia/index.asp?codigo_sophia=1')

#Identifica o frame onde os metadados estão
frame = firefox.find_element_by_tag_name("frameset").find_element_by_tag_name("frame")

#Identificar qual documento o atual
frame.get_attribute('src')

#Código para mudar de documento direto no HTML.
#firefox.execute_script("arguments[0].src = 'http://acervo.bndigital.bn.br/sophia/spacer.asp?codigo_sophia=150000';", frame)

#Direciona o drives para dentro do conteúdo do frame onde os metadados estão
firefox.switch_to.frame(frame)

#Direciona o driver para a div onde a tabela com os metadados está!
firefox.find_element_by_xpath("//*[@id='div_conteudo']")

#Identifica a tabela com os metadados na tabela com a classe max_width table-ficha-detalhes
#Nesse momento o script dá erro se o numero idnetificador não for encontrado (Previsão de 101.818 itens)
metadata = firefox.find_element_by_xpath("//*[@class='max_width table-ficha-detalhes']").get_attribute('outerHTML')

#Tranforma a tabela em um dataframe
df  = pd.read_html(metadata)
result_table= df[0]

#Colunas com os resultados (Coluna 1 metadados e coluna 2 valores).
result_table[[1,2]]
