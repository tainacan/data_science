#!/usr/bin/env python
# coding: utf-8

import requests
from collections import defaultdict
from bs4 import BeautifulSoup
import pandas as pd

endpoint_exhibits = 'http://bdce.unb.br/api/exhibit_pages'
response = requests.get(endpoint_exhibits)
exhibits = response.json()
exhibit_dict = defaultdict(list)

for exhibit in exhibits:
    exhibit_dict['page_id'].append(exhibit['id'])
    exhibit_dict['page_title'].append(exhibit['title'])
   
    exhibit_response = requests.get(exhibit['exhibit']['url'])
    exhibit_source = exhibit_response.json()
    
    exhibit_dict['exhibit_title'].append(exhibit_source['title'])
    clean_description = BeautifulSoup(exhibit_source['description'], "lxml").text
    exhibit_dict['exhibit_description'].append(clean_description)

exhibit_df = pd.DataFrame(exhibit_dict)
exhibit_df.to_csv('bdce_omeka_exhibits.csv')
