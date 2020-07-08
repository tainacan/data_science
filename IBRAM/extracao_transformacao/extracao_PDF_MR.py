#Bblioteca para extraçao do texto do PDF.
import PyPDF2
#Biblioteca para extrair padrões de texto.
import re
#Biblioteca para listar ps múltiplos PDFs.
import glob
#Biblioteca para criar e salvar os dados no CSV.
import csv

#Dicionário de regex para buscar no PDF os valores dos metadados buscados.
#Os regex são baseados na lógica de obter uma string entre outras duas strings.
match_dict = {
    'Num.Ref.':'(?<=Num.Ref.: \n)((.|\n)*)(?=Nº Inventário: )',
    'Data':'(?<=Data: \n)((.|\n)*)(?=Locais: \n)',
    'Procedência':'(?<=Procedência: \n)((.|\n)*)(?=Aquisição: \n)',
    'Aquisição':'(?<=Aquisição: \n)((.|\n)*)(?=Números Antigos: \n)',
    'Números Antigos':'(?<=Números Antigos: \n)((.|\n)*)(?=Guarda Atual: \n)',    
}

#Acessa cada PDF.
for file_name in glob.glob("PDFS\\*.pdf"):
    file_name = file_name.strip('PDFS\\').strip('.pdf')
    print('\n###Lendo o PDF {}###\n'.format(file_name))
    
    #Abre o PDF
    pdfFileObj= open('PDFS\\{}.pdf'.format(file_name),'rb')
    #Lê o PDF
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    #Pega o Número de Páginas
    n_pages = pdfReader.getNumPages()
    
    #Escreve os dados em um CSV.
    with open('resultado.csv'.format(file_name), mode='a', encoding= 'utf-8', newline='') as csv_output:
        csv_output_writer = csv.writer(csv_output)
        csv_output_writer.writerow(['Num.Ref.','Data','Procedência','Aquisição','Números Antigos'])

        #Itera por cada página do PDF
        for page in range(n_pages):
            print('Extraindo Texto da Página {}/{}'.format(page,n_pages))

            #Pega a página do PDF
            pageObj = pdfReader.getPage(page)

            #Extrai o texto da página do PDF
            text = pageObj.extractText()

            print('Texto extraído da página {}'.format(page))

            #Inicia uma lista para adicionar os matches.
            lista_results = []

            #Pega a regex de cada metadado do diconário de regex.
            for metadata in match_dict.keys():
                match = re.search(match_dict[metadata], text)

                #Se o resultado da match for nulo, adiciona o valor None na lista de resultados.
                if match == None:
                    lista_results.append('None')
                    
                #Remove um lixo (nova linha) existente nos metadados Num.Ref e Data, e adiciona os valores limpos na lista.
                elif metadata == 'Num.Ref.' or metadata == 'Data':
                    lista_results.append(match[0].replace('\n',''))

                #Se não ocorrer os casos anteriores adiciona os valores na lista.
                else:
                    lista_results.append(match[0])

            print('Valores Obtidos na página {}: {}'.format(page,lista_results))

            #Verifica se todos os valores obtidos foram nulos e não escreve no CSV. (No caso de páginas do PDF que não tem esses valores)
            if list(set(lista_results)) == ['None']:
                print('Lista Vazia, pulando...')
                continue

            #Escreve a lista no CSV
            else:
                print('Lista Válida, adicionando...')
                csv_output_writer.writerow(lista_results)

            #Limpa a lista dos valores ja adicionados ao CSV para usá-la novamente na próxima página.
            del lista_results[:]
