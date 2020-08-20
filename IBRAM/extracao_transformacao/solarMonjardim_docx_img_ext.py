# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 15:41:07 2020

@author: luisr
"""
import zipfile
import os
import shutil
from tqdm import tqdm #adiciona uma barra de "loading"
import glob

#%%
srcPath = ""
imgsPath = ""
#%%
def extractimgs(docxpath, dstpath):
    
    doc = zipfile.ZipFile(docxpath)
    
    for info in doc.infolist():
       
       if info.filename.endswith((".png", ".jpeg", ".gif")):
           
           if info.filename.split("/")[-1] == "image1.png" or info.filename.split("/")[-1] == "image2.png":
               
               continue
           
           else:
               
               doc.extract(info.filename, dstpath)
               shutil.copy(dstpath+"\\"+info.filename, dstpath+"\\"+ docxpath.split("\\")[-1].strip('.docx') + "_" + info.filename.split("/")[-1])

    doc.close()
#%%
for infile in tqdm(glob.glob(os.path.join(srcPath, '*.docx') ), desc="processando dados", unit="files"):
    extractimgs(infile, imgsPath)
    
    