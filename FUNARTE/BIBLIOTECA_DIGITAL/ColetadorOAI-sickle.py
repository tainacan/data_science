from typing import List, Any

import streamlit as st
import pandas as pd

# Biblioteca utilizada - https://sickle.readthedocs.io/en/latest/installation.html
from sickle import Sickle

# Cabeçalho da aplicação - Banner Funarte e imagens gerais
from PIL import Image


# *************************************************************************
# Função para disparar ação de coletar PROVEDORES DE TESES E DISSERTACOES
# *************************************************************************
def coletar_BDTD(provedores, nomearquivo):
    # cria o dataframe para guardar o resultado da coleta
    resultado = pd.DataFrame(
        columns=['title', 'creator', 'contributor', 'subject', 'description', 'coverage', 'date', 'format',
                 'identifier',
                 'language', 'provider', 'publisher', 'relation', 'rights', 'source', 'type', 'setSpec'])

    st.write('Iniciando a coleta....')
    contadorgeral = 0  # conta o total de registros coletados de todos os provedores

    for n in range(len(provedores['provider'])):  # percorre a planilha dos provedores

        try:
            provider = provedores['provider'][n]  # armazena a sigla da instituição
            url_provider = provedores['url_provider'][n]  # armazena a url do provedor
            set_list = provedores['setSpec'][n].split(",")  # recupera as comunidades a serem coletadas

            st.write('Coletando o provedor : ', provider)

            # inicializa o provedor
            sickle = Sickle(url_provider)
            identify = sickle.Identify()  # identifica o provedor e já verifica se está respondendo no endpoint
            if (identify):

                # itera pelos conjuntos de um provedor já reconhecido como ativo
                for conjunto in set_list:
                    st.write('Coletando o conjunto : ', conjunto)

                    # Tenta coletar o conjunto de registros especificados
                    # Pode resultar em erro caso o conjunto de registros retorne 0 como resultado
                    try:
                        registros = sickle.ListRecords(
                            **{'metadataPrefix': 'oai_dc', 'set': conjunto, 'from': ano + '-01-01'})
                        contador = 0

                        # itera pelo conjunto de registros identificados
                        for registro in registros:
                            contador = contador + 1

                            # recupera os metadados de cada registro em formato dicionario
                            metadados = registro.metadata

                            # recupera os metadados individualmente.
                            # Os campos podem ser multivalorados. Para isso, é preciso extrair item por item da lista de cada metadado.
                            # Também precisa tratar exceção para caso o metadado não exista no repositório
                            title = 'DADO AUSENTE NO PROVEDOR'
                            creator = 'DADO AUSENTE NO PROVEDOR'
                            contributor = 'DADO AUSENTE NO PROVEDOR'
                            subject = 'DADO AUSENTE NO PROVEDOR'
                            description = 'DADO AUSENTE NO PROVEDOR'
                            coverage = 'DADO AUSENTE NO PROVEDOR'
                            datem = 'DADO AUSENTE NO PROVEDOR'
                            formatm = 'DADO AUSENTE NO PROVEDOR'
                            identifier = 'DADO AUSENTE NO PROVEDOR'
                            language = 'DADO AUSENTE NO PROVEDOR'
                            provider = 'DADO AUSENTE NO PROVEDOR'
                            publisher = 'DADO AUSENTE NO PROVEDOR'
                            relation = 'DADO AUSENTE NO PROVEDOR'
                            rights = 'DADO AUSENTE NO PROVEDOR'
                            source = 'DADO AUSENTE NO PROVEDOR'
                            typem = 'DADO AUSENTE NO PROVEDOR'
                            setSpec = 'DADO AUSENTE NO PROVEDOR'

                            # METADADO TITLE
                            if 'title' in metadados:
                                i = 0
                                for titulo in metadados['title']:
                                    if i == 0:
                                        title = titulo
                                        i = i + 1
                                    else:
                                        title = title + "||" + titulo

                            # METADADO CREATOR
                            if 'creator' in metadados:
                                i = 0
                                for criador in metadados['creator']:
                                    if i == 0:
                                        creator = criador
                                        i = i + 1
                                    else:
                                        creator = creator + "||" + criador

                            # METADADO CONTRIBUTOR
                            if 'contributor' in metadados:
                                i = 0
                                for contribuidor in metadados['contributor']:
                                    if i == 0:
                                        contributor = contribuidor
                                        i = i + 1
                                    else:
                                        contributor = contributor + "||" + contribuidor

                            # METADADO SUBJECT
                            if 'subject' in metadados:
                                i = 0
                                for assunto in metadados['subject']:
                                    if i == 0:
                                        subject = assunto
                                        i = i + 1
                                    else:
                                        subject = subject + "||" + assunto

                            # METADADO DESCRIPTION
                            if 'description' in metadados:
                                i = 0
                                for descricao in metadados['description']:
                                    if i == 0:
                                        description = descricao
                                        i = i + 1
                                    else:
                                        description = description + "||" + descricao

                            # METADADO COVERAGE
                            if 'coverage' in metadados:
                                i = 0
                                for cobertura in metadados['coverage']:
                                    if i == 0:
                                        coverage = cobertura
                                        i = i + 1
                                    else:
                                        coverage = coverage + "||" + cobertura

                            # METADADO DATE
                            if 'date' in metadados:
                                i = 0
                                for data in metadados['date']:
                                    if i == 0:
                                        datem = data
                                        i = i + 1
                                    else:
                                        datem = datem + "||" + data

                            # METADADO FORMAT
                            if 'format' in metadados:
                                i = 0
                                for formato in metadados['format']:
                                    if i == 0:
                                        formatm = formato
                                        i = i + 1
                                    else:
                                        formatm = format + "||" + formato

                            # METADADO IDENTIFIER
                            if 'identifier' in metadados:
                                i = 0
                                for ide in metadados['identifier']:
                                    if i == 0:
                                        identifier = ide
                                        i = i + 1
                                    else:
                                        identifier = identifier + "||" + ide

                            # METADADO LANGUAGE
                            if 'language' in metadados:
                                i = 0
                                for lingua in metadados['language']:
                                    if i == 0:
                                        language = lingua
                                        i = i + 1
                                    else:
                                        language = language + "||" + lingua

                            # METADADO PROVIDER
                            if 'provider' in metadados:
                                i = 0
                                for provedor in metadados['provider']:
                                    if i == 0:
                                        provider = provedor
                                        i = i + 1
                                    else:
                                        provider = provider + "||" + provedor
                            else:
                                provider = provedores['provider'][n]

                            # METADADO PUBLISHER
                            if 'publisher' in metadados:
                                i = 0
                                for publicador in metadados['publisher']:
                                    if i == 0:
                                        publisher = publicador
                                        i = i + 1
                                    else:
                                        publisher = publisher + "||" + publicador

                            # METADADO RELATION
                            if 'relation' in metadados:
                                i = 0
                                for relacao in metadados['relation']:
                                    if i == 0:
                                        relation = relacao
                                        i = i + 1
                                    else:
                                        relation = relation + "||" + relacao

                            # METADADO RIGHTS
                            if 'rights' in metadados:
                                i = 0
                                for direitos in metadados['rights']:
                                    if i == 0:
                                        rights = direitos
                                        i = i + 1
                                    else:
                                        rights = rights + "||" + direitos

                            # METADADO SOURCE
                            if 'source' in metadados:
                                i = 0
                                for fonte in metadados['source']:
                                    if i == 0:
                                        source = fonte
                                        i = i + 1
                                    else:
                                        source = source + "||" + fonte

                            # METADADO TYPE
                            if 'type' in metadados:
                                i = 0
                                for tipo in metadados['type']:
                                    if i == 0:
                                        typem = tipo
                                        i = i + 1
                                    else:
                                        typem = typem + "||" + tipo

                            setSpec = conjunto

                            # monta dataframe com os metadados coletados
                            metadadoscoletados = [
                                [title, creator, contributor, subject, description, coverage, datem, formatm,
                                 identifier, language, provider, publisher, relation, rights, source, typem, setSpec]]

                            dadoscoletados = pd.DataFrame(metadadoscoletados,
                                                          columns=['title', 'creator', 'contributor', 'subject',
                                                                   'description', 'coverage', 'date', 'format',
                                                                   'identifier', 'language', 'provider', 'publisher',
                                                                   'relation', 'rights', 'source', 'type', 'setSpec'])

                            # inclui os resultados no dataframe
                            resultado = pd.concat([resultado, dadoscoletados], sort=False)

                        st.write('Registros coletados : ', contador)

                        contadorgeral = contadorgeral + contador

                    except Exception as e:
                        st.write('Sem atualizações no conjunto : ', conjunto)
                        continue

                st.write('**************************************************************')

        except Exception as e:
            print(e)
            st.write('Erro no provedor')
            st.write('**************************************************************')
            continue

    st.write(resultado['provider'].value_counts())
    st.write('TOTAL DE REGISTROS COLETADOS DE TODOS OS PROVEDORES: ', contadorgeral)
    st.write('************** FIM DA COLETA **************')

    resultado.to_csv(nomearquivo, index=False)


# *************************************************************************
# FIM DA Função para disparar ação de coletar PROVEDORES DE TESES E DISSERTACOES
# *************************************************************************

# *************************************************************************
# Função para disparar ação de coletar PROVEDORES DE PERIODICOS
# *************************************************************************
def coletar_PERIODICO(provedores, nomearquivo):
    # cria o dataframe para guardar o resultado da coleta
    resultado = pd.DataFrame(
        columns=['title', 'creator', 'contributor', 'subject', 'description', 'coverage', 'date', 'format',
                 'identifier',
                 'language', 'provider', 'publisher', 'relation', 'rights', 'source', 'type', 'setSpec'])

    st.write('Iniciando a coleta....')
    contadorgeral = 0  # conta o total de registros coletados de todos os provedores

    for n in range(len(provedores['titulo'])):  # percorre a planilha dos provedores

        try:
            provider = provedores['titulo'][n]  # armazena a sigla da instituição
            url_provider = provedores['url'][n]  # armazena a url do provedor

            st.write('Coletando o provedor : ', provider)

            # inicializa o provedor
            sickle = Sickle(url_provider)
            identify = sickle.Identify()  # identifica o provedor e já verifica se está respondendo no endpoint
            if (identify):

                sets = sickle.ListSets()
                for conjuntorevista in sets:
                    conjunto = conjuntorevista.setSpec

                    st.write("Coletando o conjunto: ", conjunto)

                    # Tenta coletar o conjunto de registros especificados
                    # Pode resultar em erro caso o conjunto de registros retorne 0 como resultado
                    try:
                        registros = sickle.ListRecords(
                            **{'metadataPrefix': 'oai_dc', 'set': conjunto, 'from': ano + '-01-01'})
                        contador = 0

                        # itera pelo conjunto de registros identificados
                        for registro in registros:
                            contador = contador + 1

                            # recupera os metadados de cada registro em formato dicionario
                            metadados = registro.metadata

                            # recupera os metadados individualmente.
                            # Os campos podem ser multivalorados. Para isso, é preciso extrair item por item da lista de cada metadado.
                            # Também precisa tratar exceção para caso o metadado não exista no repositório
                            title = 'DADO AUSENTE NO PROVEDOR'
                            creator = 'DADO AUSENTE NO PROVEDOR'
                            contributor = 'DADO AUSENTE NO PROVEDOR'
                            subject = 'DADO AUSENTE NO PROVEDOR'
                            description = 'DADO AUSENTE NO PROVEDOR'
                            coverage = 'DADO AUSENTE NO PROVEDOR'
                            datem = 'DADO AUSENTE NO PROVEDOR'
                            formatm = 'DADO AUSENTE NO PROVEDOR'
                            identifier = 'DADO AUSENTE NO PROVEDOR'
                            language = 'DADO AUSENTE NO PROVEDOR'
                            provider = 'DADO AUSENTE NO PROVEDOR'
                            publisher = 'DADO AUSENTE NO PROVEDOR'
                            relation = 'DADO AUSENTE NO PROVEDOR'
                            rights = 'DADO AUSENTE NO PROVEDOR'
                            source = 'DADO AUSENTE NO PROVEDOR'
                            typem = 'DADO AUSENTE NO PROVEDOR'

                            # METADADO TITLE
                            if 'title' in metadados:
                                i = 0
                                for titulo in metadados['title']:
                                    if i == 0:
                                        title = titulo
                                        i = i + 1
                                    else:
                                        title = title + "||" + titulo

                            # METADADO CREATOR
                            if 'creator' in metadados:
                                i = 0
                                for criador in metadados['creator']:
                                    if i == 0:
                                        creator = criador
                                        i = i + 1
                                    else:
                                        creator = creator + "||" + criador

                            # METADADO CONTRIBUTOR
                            if 'contributor' in metadados:
                                i = 0
                                for contribuidor in metadados['contributor']:
                                    if i == 0:
                                        contributor = contribuidor
                                        i = i + 1
                                    else:
                                        contributor = contributor + "||" + contribuidor

                            # METADADO SUBJECT
                            if 'subject' in metadados:
                                i = 0
                                for assunto in metadados['subject']:
                                    if i == 0:
                                        subject = assunto
                                        i = i + 1
                                    else:
                                        subject = subject + "||" + assunto

                            # METADADO DESCRIPTION
                            if 'description' in metadados:
                                i = 0
                                for descricao in metadados['description']:
                                    if i == 0:
                                        description = descricao
                                        i = i + 1
                                    else:
                                        description = description + "||" + descricao

                            # METADADO COVERAGE
                            if 'coverage' in metadados:
                                i = 0
                                for cobertura in metadados['coverage']:
                                    if i == 0:
                                        coverage = cobertura
                                        i = i + 1
                                    else:
                                        coverage = coverage + "||" + cobertura

                            # METADADO DATE
                            if 'date' in metadados:
                                i = 0
                                for data in metadados['date']:
                                    if i == 0:
                                        datem = data
                                        i = i + 1
                                    else:
                                        datem = datem + "||" + data

                            # METADADO FORMAT
                            if 'format' in metadados:
                                i = 0
                                for formato in metadados['format']:
                                    if i == 0:
                                        formatm = formato
                                        i = i + 1
                                    else:
                                        formatm = format + "||" + formato

                            # METADADO IDENTIFIER
                            if 'identifier' in metadados:
                                i = 0
                                for ide in metadados['identifier']:
                                    if i == 0:
                                        identifier = ide
                                        i = i + 1
                                    else:
                                        identifier = identifier + "||" + ide

                            # METADADO LANGUAGE
                            if 'language' in metadados:
                                i = 0
                                for lingua in metadados['language']:
                                    if i == 0:
                                        language = lingua
                                        i = i + 1
                                    else:
                                        language = language + "||" + lingua

                            # METADADO PROVIDER
                            if 'provider' in metadados:
                                i = 0
                                for provedor in metadados['provider']:
                                    if i == 0:
                                        provider = provedor
                                        i = i + 1
                                    else:
                                        provider = provider + "||" + provedor
                            else:
                                provider = provedores['titulo'][n]

                            # METADADO PUBLISHER
                            if 'publisher' in metadados:
                                i = 0
                                for publicador in metadados['publisher']:
                                    if i == 0:
                                        publisher = publicador
                                        i = i + 1
                                    else:
                                        publisher = publisher + "||" + publicador

                            # METADADO RELATION
                            if 'relation' in metadados:
                                i = 0
                                for relacao in metadados['relation']:
                                    if i == 0:
                                        relation = relacao
                                        i = i + 1
                                    else:
                                        relation = relation + "||" + relacao

                            # METADADO RIGHTS
                            if 'rights' in metadados:
                                i = 0
                                for direitos in metadados['rights']:
                                    if i == 0:
                                        rights = direitos
                                        i = i + 1
                                    else:
                                        rights = rights + "||" + direitos

                            # METADADO SOURCE
                            if 'source' in metadados:
                                i = 0
                                for fonte in metadados['source']:
                                    if i == 0:
                                        source = fonte
                                        i = i + 1
                                    else:
                                        source = source + "||" + fonte

                            # METADADO TYPE
                            if 'type' in metadados:
                                i = 0
                                for tipo in metadados['type']:
                                    if i == 0:
                                        typem = tipo
                                        i = i + 1
                                    else:
                                        typem = typem + "||" + tipo

                            setSpec = conjunto

                            # monta dataframe com os metadados coletados
                            metadadoscoletados = [
                                [title, creator, contributor, subject, description, coverage, datem, formatm,
                                 identifier, language, provider, publisher, relation, rights, source, typem, setSpec]]

                            dadoscoletados = pd.DataFrame(metadadoscoletados,
                                                          columns=['title', 'creator', 'contributor', 'subject',
                                                                   'description', 'coverage', 'date', 'format',
                                                                   'identifier', 'language', 'provider', 'publisher',
                                                                   'relation', 'rights', 'source', 'type', 'setSpec'])

                            # inclui os resultados no dataframe
                            resultado = pd.concat([resultado, dadoscoletados], sort=False)

                        st.write('Registros coletados : ', contador)

                        contadorgeral = contadorgeral + contador

                    except Exception as e:
                        st.write('Sem atualizações no provedor : ', provider)
                        st.write('**************************************************************')
                        continue

            st.write('**************************************************************')

        except Exception as e:
            print(e)
            st.write('Erro no provedor')
            st.write('**************************************************************')
            continue

    st.write(resultado['provider'].value_counts())
    st.write('TOTAL DE REGISTROS COLETADOS DE TODOS OS PROVEDORES: ', contadorgeral)
    st.write('************** FIM DA COLETA **************')

    resultado.to_csv(nomearquivo, index=False)


# *************************************************************************
# FIM DA Função para disparar ação de coletar PROVEDORES DE PERIODICOS
# *************************************************************************


# *************************************************************************
# Função para ajustar documentos a data do ano desejado - SOMENTE PARA PERIÓDICOS
# *************************************************************************
def ajustardata_PERIODICO(nomearquivo, ano):
    st.write("Iniciando ajuste de datas ao ano:", ano)
    periodicos = pd.read_csv(nomearquivo)  # coleta arquivo de periodicos
    st.write("Síntese dos dados coletados:")
    st.write(periodicos['provider'].value_counts())  # apresenta síntese por provedores
    totaldeitens = len(periodicos.index)  # calcula total de itens no dataframe
    st.write("Total de registros coletados:", totaldeitens)
    for i in periodicos.index:
        data = periodicos['date'][i]
        anodocumento = data[0:4]
        if (anodocumento != ano):
            periodicos = periodicos.drop(i)
    st.write('**************************************************************')
    st.write("Síntese dos dados ajustados:")
    st.write(periodicos['provider'].value_counts())
    totaldeitens = len(periodicos.index)  # calcula total de itens no dataframe
    st.write("Total de registros ajustados:", totaldeitens)
    st.write('**************************************************************')
    st.write("Base de dados final depois do ajuste de data ao ano da coleta:")
    st.write(periodicos)
    periodicos.to_csv(nomearquivo, index=False)


# *************************************************************************
# FIM DA Função para ajustar documentos a data do ano desejado - SOMENTE PARA PERIÓDICOS
# *************************************************************************

# *************************************************************************
# Função para filtro temático de artigos científicos - SOMENTE PARA PERIÓDICOS
# *************************************************************************
def filtra_artigo():
    st.write("Iniciando filtragem temático de artigos")
    st.text("Confira o vocabulário controlado:")
    vocabulario = pd.read_excel('VOCABCONTROLADO.XLSX')
    st.write(vocabulario)

    artigos = pd.read_csv('resultadoPERIODICOS.csv')
    totaldeitens = len(artigos.index)  # calcula total de itens no dataframe
    st.write("Total de registros a filtrar:", totaldeitens)

    for i in artigos.index:
        texto = str(artigos['title'][i])+' '+str(artigos['subject'][i])+' '+str(artigos['description'][i])
        texto = texto.lower()
        existetermo = 0
        for j in vocabulario.index:
            termo = vocabulario['Termos'][j]
            termo = termo.lower()
            if termo in texto:
               existetermo = 1
        if existetermo == 0:
            artigos = artigos.drop(i)
    st.write('**************************************************************')
    st.write("Síntese dos dados filtrados:")
    st.write(artigos['provider'].value_counts())
    totaldeitens = len(artigos.index)  # calcula total de itens no dataframe
    st.write("Total de registros ajustados:", totaldeitens)
    st.write('**************************************************************')
    artigos.to_csv('resultadoPERIODICOS.csv', index=False)


# *************************************************************************
# INTERFACE GRÁFICA DO APLICATIVO
# *************************************************************************
# INFORMAÇÕES NA ÁREA CENTRAL DO APLICATIVO
image = Image.open('cabecalhofunarte.jpeg')
st.image(image, caption='')
st.title('Coletor OAI-PMH')
st.subheader("Artigos científicos, teses e dissertações do campo das Artes")

# INFORMAÇÕES NA SIDEBAR DO APLICATIVO
# Coleta ano para filtro dos resultados
st.sidebar.subheader("Configurações:")
ano = st.sidebar.text_input('Definir ano da coleta (digitar ano completo)', '')
st.sidebar.write('Ano definido para coleta:', ano)
# Carrega o arquivo com a lista dos endpoints OAI-PMH
uploaded_file = st.sidebar.file_uploader(
    "Selecione o arquivo com a lista de provedores de Teses/Dissertações ou Artigos científicos")
if uploaded_file is not None:
    provedores = pd.read_csv(uploaded_file)
    st.text("Confira a lista de provedores")
    st.write(provedores)
st.sidebar.write('*******')
st.sidebar.subheader("Sessão Teses e Dissertações:")
if st.sidebar.button('Coletar TESES e DISSERTAÇÕES'):
    coletar_BDTD(provedores, 'resultadoBDTD.csv')
st.sidebar.write('******')
st.sidebar.subheader("Sessão Periódicos:")
if st.sidebar.button('Coletar ARTIGOS CIENTÍFICOS'):
    coletar_PERIODICO(provedores, 'resultadoPERIODICOS.csv')
if st.sidebar.button('Ajustar data ARTIGOS CIENTÍFICOS'):
    ajustardata_PERIODICO('resultadoPERIODICOS.csv', ano)
if st.sidebar.button('Filtrar ARTIGOS CIENTÍFICOS por tema'):
    filtra_artigo()

st.sidebar.write('******')
st.text('Desenvolvido por Laboratório de Inteligência de Redes (UnB, IBICT, 2022)')
