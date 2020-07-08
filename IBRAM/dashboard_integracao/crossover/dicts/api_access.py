# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 16:36:27 2020

@author: Luis
"""

install_dict = {
        "id":["1","2","3","4","5","6","7","8", "9", "10", "11", "12"],
        "name":["Museu Victor Meirelles", "Museu Histórico Nacional", "Museu do Diamante", "Museu do Ouro",
                "Museu Regional Casa dos Ottoni", "Museu de Itaipu", "Museus de Goiás", "Museu das Missões",
                "Museu Benjamin Constant", "Museu Regional de São João Del Rei", "Museu da Inconfidência", "Museu Villa Lobos"],
        "url":["http://museuvictormeirelles.acervos.museus.gov.br", "http://mhn.acervos.museus.gov.br", 
               "http://museudodiamante.acervos.museus.gov.br", "http://museudoouro.acervos.museus.gov.br",
               "http://museuregionalcasadosottoni.acervos.museus.gov.br", "http://museudearqueologiadeitaipu.museus.gov.br", 
               "http://museusibramgoias.acervos.museus.gov.br", "http://museudasmissoes.acervos.museus.gov.br",
               "http://museucasabenjaminconstant.acervos.museus.gov.br", "http://museuregionaldesaojoaodelrei.acervos.museus.gov.br/",
               "http://museudainconfidencia.acervos.museus.gov.br/", "http://museuvillalobos.acervos.museus.gov.br"]
        }

dict_endpoint = {
"col_endpoint":"/wp-json/tainacan/v2/collections/",
"meta_endpoint":"/wp-json/tainacan/v2/collection/{}/metadata/?perpage=100",
"tax_endpoint":"/wp-json/tainacan/v2/taxonomies/",
"item_endpoint":"/wp-json/tainacan/v2/collection/{}/items/?perpage={}&paged={}",
"terms_endpoint":"/wp-json/tainacan/v2/taxonomy/{}/terms",
"term_endpoint":"/wp-json/tainacan/v2/taxonomy/{}/terms/{}"}
