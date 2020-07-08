# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 09:45:27 2019

@author: Luis
"""
import glob
import csv
import os
from collections import defaultdict

path_to_imgs = ""
imgs_format = ""
separator = ""

img_names = []
list_img = []
ids_dict = {}
links_dict = defaultdict(list)

# Para alterar o separador das imagens para espaço.
"""
for f in glob.glob(path_to_imgs+imgs_format):
    new_filename = f.replace(separator," ")
    os.rename(f,new_filename)

"""

img_names = glob.glob(path_to_imgs+imgs_format)

#Descobrir qual o special_document

for img in img_names:
    
    if " " in img: #itens com anexos
        img_id = img.split(" ")
        links_dict[img_id[0].strip(path_to_imgs)].append(img.strip(path_to_imgs))
        
    else:
        links_dict[img.strip(path_to_imgs).strip(imgs_format)].append(img.strip(path_to_imgs))


with open('link_imgs_MPI.csv', 'w', encoding = "utf-8", newline='') as out_file:
    writer = csv.writer(out_file, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['id','special_document','special_attachments'])
    
    for k in links_dict.keys():
        print("Verificando ID -",k)
        parts_list = []
        special_document = ""
        
        for part in links_dict[k]:
               
            if " " in part:
                
                new_part = part.split(" ")
                parts_list.append(int(new_part[1].strip(imgs_format)))
                
            else:
                special_document = part
                
                
        list(set(parts_list))
        if special_document == "":
            min_value = " "+str(min(parts_list))+imgs_format
            
            for part in links_dict[k]:
                   
                if min_value in part:
                    special_document = part
        
        
        links_dict[k].remove(special_document)
        
        special_attachments = "||".join(links_dict[k])
        
        writer.writerow([k,"file:"+special_document, special_attachments])
