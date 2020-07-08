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

#Escreve os dados em um CSV.
with open('resultado.csv'.format(file_name), mode='a', encoding= 'utf-8', newline='') as csv_output:
    csv_output_writer = csv.writer(csv_output)
    csv_output_writer.writerow(['Num.Ref.','Data','Procedência','Aquisição','Números Antigos'])

    #Acessa cada PDF.
    for file_name in glob.glob("PDFS\\*.pdf"):
        file_name = file_name.strip('PDFS\\').strip('.pdf')
        print('\n###Lendo o PDF {}###\n'.format(file_name))

        #Dicionário para armazenar os resultados. Resetado para cada arquivo PDF.
        result_dict = {}

        #Abre o PDF
        pdfFileObj= open('PDFS\\{}.pdf'.format(file_name),'rb')
        #Lê o PDF
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        #Pega o Número de Páginas
        n_pages = pdfReader.getNumPages()
    
        #Teste obter os dados do PDF.
        for page in range(n_pages):
            print('Extraindo Texto da Página {}/{}'.format(page,n_pages))

            #Pega a página do PDF
            pageObj = pdfReader.getPage(page)

            #Extrai o texto da página do PDF
            text = pageObj.extractText()

            print('Texto extraído da página {}'.format(page))
            
            #Pega a regex de cada metadado do diconário de regex.
            for metadata in match_dict.keys():
                match = re.search(match_dict[metadata], text)
                
                if metadata == 'Num.Ref.' and match != None:
                    num_ref = match[0].replace('\n','')
                    result_dict[num_ref] = {}
                

                elif metadata != 'Num.Ref.' and metadata not in result_dict[num_ref]:

                    if match == None:
                        result_dict[num_ref][metadata] = 'None'

                    else:
                        result_dict[num_ref][metadata] = match[0]

                elif metadata != 'Num.Ref.' and metadata in result_dict[num_ref] and metadata in result_dict[num_ref] != None:

                    if match == None:
                        continue

                    else:
                        result_dict[num_ref][metadata] = match[0]

        
        for k, v in result_dict.items():
            row = k + "||" + "||".join(list(v.values()))
            csv_output_writer.writerow(row.split("||"))
