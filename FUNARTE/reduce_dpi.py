from PIL import Image
import glob, os
import pandas as pd
outputDf = pd.DataFrame()

sourcePath = ""
destPath = ""
os.chdir(sourcePath)

for file in glob.glob("*.jpeg"):
    try:
        print(file)
        im = Image.open(file)
        im.save(destPath+file.strip(".jpeg")+".jpeg", dpi=(72, 72))
    except:
        print("ERRO: ", file)
        filesDict = {}
        filesDict['lack'] = file
        outputDf = outputDf.append(filesDict, ignore_index=True)

#%%
outputDf.to_csv("lack_images.csv")
