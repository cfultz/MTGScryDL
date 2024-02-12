import requests
from requests import get
from json import loads
import pandas as pd
import time
from shutil import copyfileobj

# Load card ID's from CSV
df = pd.read_csv('/home/cfultz/Code/MTG/all_cards.csv')
df = df[['Scryfall ID']]
df.to_csv('/home/cfultz/Code/MTG/scryfall_only.csv', index=False)

print("File converted")
time.sleep(2)

scryfall_ids = "/home/cfultz/Code/MTG/ids.txt"
print("Converting 'scryfall_only.csv' to txtfile")
time.sleep(2)
with open(scryfall_ids, 'a') as f:
    df_string = df.to_string(header=False, index=False)
    f.write(df_string)

print("Starting Loop")
time.sleep(2)
file1 = open(scryfall_ids, 'r')
count = 0


for line in file1:
    time.sleep(0.25)
    count += 1
# Load the card data from Scryfall
    card_info = loads(get(f"https://api.scryfall.com/cards/"+line.strip()).text)
    special_characters=["$", "'","`","%","&","(",")",",",":","?","!","@",",",".","*","-","/","//"]
    mtg_name = card_info['name']
    mtg_set = card_info["set"]
    for i in special_characters:
        cName = mtg_name.replace(i,"")
        cName = cName.replace(" ", "")
    try:
        mtg_img = card_info['image_uris']['normal']
    except:
        mtg_img = card_info['card_faces'][0]['image_uris']['normal']
        with open('/home/cfultz/Code/MTG/images/multi/'+cName+'.jpg', 'wb') as out_file:
            copyfileobj(get(mtg_img, stream = True).raw, out_file)

        mtg_img2 = card_info['card_faces'][1]['image_uris']['normal']
        with open('/home/cfultz/Code/MTG/images/multi/backs/'+cName+'.jpg', 'wb') as out_file:
            copyfileobj(get(mtg_img2, stream = True).raw, out_file)
    else:
        if mtg_name == "Island" or "Moutain" or "Swamp" or "Plains" or "Forest":
            with open('/home/cfultz/Code/MTG/images/land/'+cName+"."+mtg_set+'.jpg', 'wb') as out_file:
                copyfileobj(get(mtg_img, stream = True).raw, out_file)
        else:
            with open('/home/cfultz/Code/MTG/images/single/'+cName+'.jpg', 'wb') as out_file:
                copyfileobj(get(mtg_img, stream = True).raw, out_file)

print("Done!")
time.sleep(5)
