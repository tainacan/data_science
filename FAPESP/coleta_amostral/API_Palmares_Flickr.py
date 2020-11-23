import flickr_api
import pandas as pd
from time import sleep

metadata_list = ['id','dateuploaded', 'originalformat','title','description','views','taken']
url = 'https://www.flickr.com/photos/culturanegra/'

flickr_api.set_keys(api_key = 'API_KEY', api_secret = 'API_SECRET')
#%%
user = flickr_api.Person.findByUserName("Fundação Cultural Palmares")
photos = user.getPhotos()
pages = int(photos.info.pages)
sleep(2)
#%%
resultDict = {}
resultDf = pd.DataFrame()

for page in range(pages):
    sleep(5)
    
    if page == 0: 
        print("Pulando a página 0")
        
        continue
    
    else:
        print("Coletando a página {}".format(page))
        photos = user.getPhotos(page=page)
        sleep(1)
        
        for photo in photos:
            dataResult = photo.getInfo()
            sleep(1)
            
            for metadata in metadata_list:
                resultDict[metadata]=dataResult[metadata]

            print("Foto {} coletada".format(url+resultDict['id']))
            
            resultDict['url'] = url+resultDict['id']
            resultDf = resultDf.append(resultDict, ignore_index=True)
