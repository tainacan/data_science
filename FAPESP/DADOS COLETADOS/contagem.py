# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 11:56:17 2021

@author: luisr
"""

import glob
import pandas as pd
from collections import defaultdict

resultado_dict = defaultdict(list)

for file in glob.glob("*.csv"):
    print(file.split("_")[0])
    file_df = pd.read_csv(file,sep=None, engine="python")
    
    resultado_dict[file.split("_")[0]].append(len(file_df))
 #%%   
for key in resultado_dict.keys():
    print(key,",", sum(resultado_dict[key]))