#Internal path structure 
import sys
#Adicionar o path do diretório contendo os scripts
sys.path.append('')
from dicts import api_access as api, tables, inbcm
import functions
import pandas as pd
from sqlalchemy import create_engine
from collections import defaultdict

#Acesso ao banco de dados - Substituir usuário e senha
mysqlEngine = create_engine('mysql+pymysql://user:password@localhost:3306/tainacan_api')
dbConnection = mysqlEngine.connect()

#Celan itens table
functions.truncate_table('itens')

#Celan itens_termos table
functions.truncate_table('itens_termos')

#Create metadata type dataframe
metadata_type = pd.DataFrame(columns=['instalacao', 'colecao', 'metadata', 'metadata_type'])

#Get collection table from database
collection_db = pd.read_sql_table('colecao', dbConnection)

#Get itens table from database
itens_db_col = pd.read_sql_table('itens', dbConnection)
itens_db_col = itens_db_col.drop(columns=['id'])


#Collect data installation, colections and metadata
for i in range(len(api.install_dict['id'])):
    print("Verificando a Instalação {}".format(api.install_dict['name'][i]))
    
    #Requisita os dados de coleção
    collections_resp = functions.try_request(api.install_dict["url"][i]+api.dict_endpoint['col_endpoint'])
    
    #Pula se nenhuma coleção for encontrada no endpoint
    if collections_resp.json() == []:
        print("Coleção não encontrada para a instalação {}".format(api.install_dict['name'][i]))
        continue

    #Itera entre a coleções encontradas
    for collection in collections_resp.json():
        
        #Verifica se a coleção é uma das selecionadas para compor o banco de dados integrado
        if collection['name'] in inbcm.selected_col[api.install_dict['name'][i]]:
            
            #Cria variáveis para o nome da instalação, o id da coleção e o nome da coleção
            #e chave de instalação + nome da coleção utilizada para acessar o dicionário com o crossover
            install_name = api.install_dict['name'][i]
            collection_id = collection['id']
            collection_name = collection['name']
            install_key = api.install_dict["name"][i] + "_" + collection_name
            #Pegar o novo id da coleção na base de dados
            new_col_id = collection_db.loc[(collection_db['name'] == collection_name) & (collection_db['id_instalacao'] == int(api.install_dict['id'][i]))]

            print("Verificando a coleção {}".format(collection_name))
            
            page = 1
            #Requisita os dados de item para a coleção selecionada, sendo 50 itens por página.
            items_resp = functions.try_request(api.install_dict["url"][i]+api.dict_endpoint['item_endpoint'].format(collection_id, 50, page))
           
            while items_resp.json()['items'] != []:
                print("Verificando a {}º página de itens para a coleção {}".format(page,collection_name))
                
                #Reseta o dataframe dos itens
                itens_db = pd.DataFrame(columns=itens_db_col.columns.to_list())
                
                #Itera entre os itens
                for item in items_resp.json()['items']:
                    
                    itemTermDict = inbcm.itemTermDict
                    functions.clean_dict(itemTermDict)
                                        
                    #Reseta um dicionário para obter os valores dos itens ****Fazer esse dicionário
                    itens_meta = functions.clean_dict(inbcm.itens_meta)
                    
                    #Itera entre os metadados mapeados no crossover
                    #Utiliza o campo "value_as_string" para recuperar o valor dos metadados
                    for metadata_cross in inbcm.cross_dict[install_key].keys():
                        
                        for item_metadata in item['metadata'].keys():
                            
                            #Verifica se o metadado do item foi mapeado para o crossover
                            if item['metadata'][item_metadata]['name'] == metadata_cross:

                                #Verifica se o metadado é composto por termos de taxonomias
                                if inbcm.cross_dict[install_key][metadata_cross] in inbcm.tax_meta:
                         
                                    for value in item['metadata'][item_metadata]['value_as_string'].split(" | "):
                                
                                        #Get terms table from database updated for each value
                                        terms_db = pd.read_sql_table('termos', dbConnection)
                                        
                                        #Dealing with white values:
                                        if functions.normalize(value) == '':
                                            continue
                                            
                                        #Dealing with term hierarchy
                                        if " > " in functions.normalize(value):
                                            value = value.split(" > ")[-1]
                                            
                                        value_db = terms_db.loc[terms_db['name'] == functions.normalize(value)]
                                            
                                        if value_db.size == 0:
                                            
                                            #Df to insert new terms to database
                                            insert_terms_df = pd.DataFrame(columns=terms_db.columns)
                                            
                                            new_term_id = dbConnection.execute("SELECT max(id) FROM tainacan_api.termos;").fetchone()[0]+1

                                            insert_terms_df = insert_terms_df.append({'id':new_term_id,'name':functions.normalize(value)}, ignore_index = True)
                                            
                                            insert_terms_df.to_sql('termos', dbConnection, if_exists = 'append', chunksize = 1000, index=False)
                                            
                                            #Deal with terms repeated
                                            if new_term_id in itemTermDict[inbcm.cross_dict[install_key][metadata_cross]]:
                                                continue
                                            else:
                                                itemTermDict[inbcm.cross_dict[install_key][metadata_cross]].append(new_term_id)
                                            
                                        else:
                                            
                                            #Deal with terms repeated
                                            if value_db['id'].values[0] in itemTermDict[inbcm.cross_dict[install_key][metadata_cross]]:
                                                continue
                                                
                                            else:
                                                itemTermDict[inbcm.cross_dict[install_key][metadata_cross]].append(value_db['id'].values[0])

                                #Insere os valores dos metadados do item em um dicionário auxiliar
                                else:
                                    
                                    itens_meta[inbcm.cross_dict[install_key][metadata_cross]].append(item['metadata'][item_metadata]['value_as_string'])

                            #Continua se o metadado não compões a seleção feita no crossover
                            else:
                                continue
                                
                    #No caso do metadado ser uma taxonomia
                    len_list = []
                    #Mensura a quantidade de valores em cada metadado a partir do dicionário auxiliar criado acima
                    for lista in itemTermDict.values():
                        len_list.append(len(list(set(lista))))
                    
                    # Cria um fluxo de inserção de valores na tabela de relacionamento dos metadados categoricos com os termos
                    for i_list in range(max(len_list)):
                        result_dict = defaultdict(int)
                        
                        #Cria uma dataframe para inserir os metadados categoricos no banco a cada item.
                        item_term_df = pd.DataFrame(columns=pd.read_sql_table('itens_termos', dbConnection).columns)
                        item_term_df = item_term_df.drop(columns=['id'])
    
                        #Lida com as posições dos termos nas listas de valores adicionadas ao dicionário auxiliar criado acima
                        for key in itemTermDict.keys():
                            
                            #Insere a primeira posição de valores das listas do dicionario auxiliar em um dicionário que será inserido no banco
                            if len(itemTermDict[key]) > i_list:
                                result_dict[key]= itemTermDict[key][i_list]
                        
                            else:
                                result_dict[key] = None
                        
                        #Insere os valores de relacionamento entre itens e termos no banco de dados.
                        item_term_df = item_term_df.append({'id_item':str(api.install_dict['id'][i])+str(new_col_id['id'].values[0])+str(item['id']),
                                                            'autor':result_dict['Autor'],
                                                            'classificacao':result_dict['Classificação'],
                                                            'data_producao':result_dict['Data de produção'],
                                                            'estado_conservacao':result_dict['Estado de Conservação'],
                                                            'local_producao':result_dict['Local de produção'],
                                                            'material_tecnica':result_dict['Material / Técnica'],
                                                            'situacao':result_dict['Situação']}, ignore_index=True)
        
                        #Convert the relationship DataFrame to it respective SQL Table
                        item_term_df.to_sql('itens_termos', dbConnection, if_exists = 'append', chunksize = 1000, index=False)
        
                    #Insere os itens no dataframe que irá adicionar ao banco de dados
                    itens_db = itens_db.append({'id':str(api.install_dict['id'][i])+str(new_col_id['id'].values[0])+str(item['id']),
                                                'id_colecao':new_col_id['id'].values[0],
                                                'id_instalacao':int(api.install_dict['id'][i]),
                                                'item_status':item['status'],'creation_date':item['creation_date'],
                                                'modification_date':item['modification_date'], 
                                                'document_type':item['document_type'], 'document':item['document'],
                                                'url':item['url'],
                                                'num_registro':functions.list_str(itens_meta['Número de registro']),
                                                'outros_numeros':functions.list_str(itens_meta['Outros números']),
                                                'denominacao':functions.list_str(itens_meta['Denominação']),
                                                'titulo':functions.list_str(itens_meta['Título']),
                                                'resumo_descritivo':functions.list_str(itens_meta['Resumo descritivo']),
                                                'dimensoes':functions.list_str(itens_meta['Dimensões']),
                                                'dimensoes_altura':functions.list_str(itens_meta['Dimensões - altura']),
                                                'dimensoes_largura':functions.list_str(itens_meta['Dimensões - largura']),
                                                'dimensoes_diametro':functions.list_str(itens_meta['Dimensões - diâmetro']),
                                                'dimensoes_espessura':functions.list_str(itens_meta['Dimensões - espessura']),
                                                'dimensoes_prof_comp':functions.list_str(itens_meta['Dimensões - profundidade/comprimento']),
                                                'dimensoes_peso':functions.list_str(itens_meta['Dimensões - peso']),
                                                'condicoes_repoducao':functions.list_str(itens_meta['Condições de reprodução']),
                                                'midias_relacionadas':functions.list_str(itens_meta['Mídias relacionadas'])}, ignore_index=True)
                    
                print("Inserindo a página de itens no banco de dados")
                #Convert the relationship DataFrame to it respective SQL Table
                itens_db.to_sql('itens', dbConnection, if_exists = 'append', chunksize = 1000, index=False)
                
                page+=1
                items_resp = functions.try_request(api.install_dict["url"][i]+api.dict_endpoint['item_endpoint'].format(collection_id, 50, page))
        else:
            print("***** Coleção {} não consta nas coleções selecionadas para a instalação atual*****".format(collection['name']))
            continue
