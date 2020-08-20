# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 16:19:21 2020

@author: luisr
"""
import os
from tqdm import tqdm #adiciona uma barra de "loading"
import glob
import pandas as pd
from collections import defaultdict
resultDict = defaultdict(list)
resultado = pd.DataFrame()

srcPath = ""
extension = ['*.png', '*.jpeg']

for ext in extension:
    
    auxDict = defaultdict(list)
    
    for infile in tqdm(glob.glob(os.path.join(srcPath, ext)), desc="processando dados", unit="files"):
        
        file = infile.split('\\')[-1].split("_")[0]+".docx"
        img = infile.split('\\')[-1]
        auxDict[file].append(img)
        
    for key in auxDict.keys():
        if len(auxDict[key]) > 1:
            value = "||".join(auxDict[key][1:])
        else:
            value = ""
                            
        resultado = resultado.append({'file':key, 'special_document':auxDict[key][0], 'special_attachments':value} ,ignore_index=True)

#%%
resultado.to_csv("", index = False)