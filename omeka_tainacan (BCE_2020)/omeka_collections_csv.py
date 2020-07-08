#!/usr/bin/env python
# coding: utf-8

import requests
from collections import defaultdict
import pandas as pd
import time

endpoint_collections = 'http://bdce.unb.br/api/collections'
response = requests.get(endpoint_collections)
collections = response.json()
metadatum_dict = {'Date':[], 'Creator':[], 'Publisher':[], 'Title':[], 'Subject':[]}
collection_dict = defaultdict(list)
collection_dict.update(metadatum_dict)

for collection in collections:
    
    metadata_dict = {'Date':[], 'Creator':[], 'Publisher':[], 'Title':[], 'Subject':[]}
    
    collection_dict['id'].append(collection['id'])
    collection_dict['itens_count'].append(collection['items']['count'])
    
    for metadata in collection['element_texts']:
        
        for key in metadata_dict.keys():
            
            if key == metadata['element']['name']:
                metadata_dict[key].append(metadata['text'])
            else:
                metadata_dict[key].append('')
        
    for key in metadata_dict.keys():
        
        metadata_dict[key] = list(filter(None, metadata_dict[key]))
        
        if metadata_dict[key]:
            collection_dict[key].append("||".join(set(metadata_dict[key])))
        else:
            collection_dict[key].append("".join(set(metadata_dict[key])))

export_df = pd.DataFrame(collection_dict)
export_df.to_csv('collections_omeka_export.csv')
