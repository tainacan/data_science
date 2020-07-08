import pandas as 
from querys import tables_dict
from sqlalchemy import create_engine

engine = create_engine('')
connection = engine.connect()

def query_to_dict(doc, query):
    #Utiliza a query de junção das tabelas.
    query_df = pd.read_sql_query(query.format(doc), con=connection)
    result_dict={}
    query_dict={}
    pd
    #Para cada coluna da resultante da query de junção, cria um dicionário com o nome da coluna(key), e uma lista para seus valores.
    for column in query_df.columns:
        query_dict[column] = []

        #Adiciona os valores resultantes na lista.
        for iten in query_df[column]:
            if iten == None or pd.isna(iten):
                continue
            else:
                query_dict[column].append(str(iten))
    
        query_dict[column] = set(query_dict[column])
        
        result_dict[column] = ['||'.join(query_dict[column])]
        
        result_df = pd.DataFrame.from_dict(result_dict, orient='columns')
     
    return result_df

for key in tables_dict:
    cont = 1
    print("Working on table {}".format(key))
    query_treatment = tables_dict[key].split('WHERE')
    query_treatment = query_treatment[0] +';'
    
    queryDocs_df = pd.read_sql_query(query_treatment, con=connection)
    
    lista_docs = (doc for doc in queryDocs_df['idDocumento'])
    lista_docs = set(lista_docs)
    
    for doc in lista_docs:
        print("Inserting document {}".format(doc))
        result_df = query_to_dict(doc, tables_dict[key])
        result_df.to_sql(name=key, con=connection, schema='mr_rel', if_exists='append', index=False)
        print("{} Documents Remain!".format(len(lista_docs)-cont))
        cont+=1
