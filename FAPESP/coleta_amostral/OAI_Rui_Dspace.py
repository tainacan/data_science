from sickle import Sickle as sk
import xml.etree.ElementTree as ET
from collections import defaultdict 
import pandas as pd
import time

metadata_dict = defaultdict(list)
oai_rui = pd.DataFrame()
i = 1

sickle = sk('http://rubi.casaruibarbosa.gov.br/oai/request?')
records = sickle.ListRecords(metadataPrefix='oai_dc')

for record in records:
    
    metadata_dict.clear()
    dc_dict = {}
    
    print("Coletando o registro {}".format(i))
    
    root = ET.fromstring(record.raw)
    
    try:
        metadata_dc = root[1][0]
        
        for child in metadata_dc:
            metadata_dict[child.tag].append(child.text)
        
        for key in metadata_dict.keys():
            
            if len(metadata_dict[key]) > 1:
                dc_dict[key] = "||".join(metadata_dict[key])
                
            elif len(metadata_dict[key]) == 0:
                dc_dict[key] = ""
                
            else:
                dc_dict[key] = metadata_dict[key][0]
                
        oai_rui = oai_rui.append(dc_dict, ignore_index=True)
    
    except:
        
        print(record.raw)
        continue
    
    i+=1
    
    if i == 100:
        break
    
    time.sleep(5)

oai_rui.to_csv("oai_rui.csv")
