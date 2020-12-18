

import pandas as pd
import urllib.request
import sys
import socket

socket.setdefaulttimeout(30)

dbName = 'imagens_faltantens.csv'
path_to_db = ''.format(dbName)
path_to_imgs = ''
imgDb = pd.read_csv(path_to_db)

#Function Reference: https://shakeratos.tistory.com/55
def download_file(source_url, destination_path, retries=3):
  def _progress(count, block_size, total_size):
    sys.stderr.write('\r>> Downloading %.1f%%' % (float(count * block_size) / float(total_size) * 100.0))
    sys.stderr.flush()
  
  while(retries > 0):
    try:
      urllib.request.urlretrieve(source_url, destination_path, _progress)
      break
    except:
      print("retry")
      retries = retries - 1
      continue

def setFileName(text):
    itemId = text.split('?item=')[1].split('&imagem=')[0]
    imageId = text.split('?item=')[1].split('&imagem=')[1].split('&')[0]
    return itemId + '_' + imageId + '.jpeg'

for row in range(len(imgDb['codigo'])):
    
    if "||" in imgDb['imagem'][row]:
        
        for imgLink in imgDb['imagem'][row].split("||"):
            print(imgLink,end = "\n")
            download_file(imgLink, path_to_imgs+setFileName(imgLink))
            print('\n Salvando anexo {}'.format(setFileName(imgLink)))
    else:
        print(imgDb['imagem'][row],end = "\n")
        download_file(imgDb['imagem'][row], path_to_imgs+setFileName(imgDb['imagem'][row]))
        print('\n Salvando anexo {}'.format(setFileName(imgDb['imagem'][row])))
