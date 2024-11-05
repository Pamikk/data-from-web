from annotator import get_response,encode_image
import pandas as pd
path = './n5k/dish_metadata_cafe1.csv'
img_path = './n5k'
headers = ['dish_id', 'total_calories', 'total_mass', 'total_fat', 'total_carb', 'total_protein']
import os
from random import sample
def choose_cam(path):
    res=[]
    for i in ['A','B','C','D']:
        if os.path.exists(path+f'_{i}.jpeg'):
            res.append(i)
    return sample(res,1)[0]
with open(path) as f:
    for item in f.readlines():
        item = item.split(',')
        nutritions = dict(zip(headers, item[:6]))
        integredients = item[6:][1::7]
        if len(integredients)<2:
            pass
        nutritions['integredients'] = integredients
        img = encode_image(os.path.join('./n5k',item[0]+'.jpeg'))
        get_response(img, nutritions)
        exit()