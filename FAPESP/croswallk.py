#creators daltonmartins / luisfeliperd

import pandas as pd
import glob # biblioteca para leitura de arquivos em diretórios

dfmapeamento=pd.read_excel('mapeamento.xlsx')
def sjoin(x): return '||'.join(x[x.notnull()].astype(str)) #comando para unir os valores de colunas iguais separado por ||

for arquivo in glob.glob("./CSV/*.*"):
    df=pd.read_csv(arquivo,sep=None, engine="python") #comando que detecta o separados do CSV automaticamente
    nomescolunas=df.columns.tolist()
    
    print("**************************")
    print(arquivo)
    print()
    print("NOME DAS COLUNAS ANTES")
    print(nomescolunas)  
    
    
    for coluna in nomescolunas:
        resultado=dfmapeamento.loc[dfmapeamento['Metadados'] == coluna]
        if not(resultado.empty): #se a coluna for mapeada para DC, substitui na dataframe
            novacoluna=resultado['DC'].tolist()[0]
            df.rename(columns = {coluna: novacoluna}, inplace=True)
            print("Renomeando ", coluna, " para ",novacoluna)
        else: #se a coluna não for mapeada para DC, apaga a coluna no dataframe
            df.drop(columns=[coluna], inplace=True) #apaga a coluna
            print("Apagando ",coluna)
            
    print()
    df=df.groupby(level=0, axis=1).apply(lambda x: x.apply(sjoin, axis=1)) # agrupa as colunas e chama a função pelo lambda
    print("NOME DAS COLUNAS DEPOIS")
    nomescolunas=df.columns.tolist()
    print(nomescolunas) 
    arquivo=arquivo.strip("./CSV/").strip(".csv")
    df.to_csv(arquivo+'_DC'+".csv")
