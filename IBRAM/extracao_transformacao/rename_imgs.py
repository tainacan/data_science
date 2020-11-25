import glob
import csv
import os
from collections import defaultdict
import unidecode
import pandas as pd

newNames = pd.DataFrame()

path_to_imgs = ""
imgs_format = "*.png"
separator = " "

for f in glob.glob(path_to_imgs+imgs_format):
    ids_dict = {}
    #remove acentos e substitui espaços por _
    new_filename = unidecode.unidecode(f).replace(separator,"_")
    #substitui pontos por _
    new_filename = new_filename.strip(".png").replace(".", "_") + ".png"
    #salva um dataframe com os nomes antigos e os nomes novos
    ids_dict['nome antigo'] = f.strip(path_to_imgs)
    ids_dict['nome novo'] = new_filename.strip(path_to_imgs)
    print(new_filename.strip(path_to_imgs))
    #renomeia as imagens
    os.rename(f,new_filename)
    
    newNames = newNames.append(ids_dict, ignore_index=(True))

#%%
newNames.to_csv("")
