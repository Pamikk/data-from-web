from annotator import get_response,encode_image
import os
root_path = '/home/dataset/nutrition5k_dataset'

paths = ['metadata/dish_metadata_cafe1.csv','metadata/dish_metadata_cafe2.csv']
img_path = os.path.join(root_path,'frames')
headers = ['total_calories', 'total_mass', 'total_fat', 'total_carb', 'total_protein']
batch_size = 6
from numpy import random
random.seed(2333)
from random import sample
import csv
def choose_cam(path):
    res=[]
    for i in ['A','B','C','D']:
        if os.path.exists(path+f'_{i}.jpeg'):
            res.append(path+f'_{i}.jpeg')
    if len(res) == 0:
        return None
    return sample(res,1)[0]
from tqdm import tqdm
import time
def query_openai(cam_path,nutritions,queue=None):
    img = encode_image(cam_path)
    gen_item = None
    results = get_response(img, nutritions)
    if (len(results)>2) and (len(results)%2==0):
        num_rounds = len(results) // 2
        start = 0
        for idx,i in enumerate(results):
            if 'calorie' in i:
                start = idx//2
                break
        if start==num_rounds-1:
            sampled_round_id = num_rounds-1
        else:
            sampled_round_id = random.randint(start, num_rounds - 1) if num_rounds>1 else 0
        gen_item = {}
        gen_item["history"] = [[results[i * 2],results[i* 2 + 1]] for i in range(sampled_round_id)] if sampled_round_id > 0 else []
        gen_item["query"] = results[sampled_round_id * 2]
        gen_item["response"] = results[sampled_round_id * 2 + 1]
        gen_item["image"] =[cam_path]
    #global counter
    #with counter.get_lock():
        #counter.value += 1
    if queue and (gen_item):
        queue.put(gen_item)
    else:
        return gen_item
import csv
import sys
def batch_query(data,idx):
    res=[]
    for i,item in enumerate(data):
        if (i%100==0):
            if res:
                print(idx,res[-1],len(res))
            print(f'{idx}:{i}/{len(data)}')
            sys.stdout.flush()
        nutritions = dict(zip(headers, item[1:6]))
        ingredients = item[6:][1::7]  # Extract ingredients from the CSV row

        # Skip entries with insufficient ingredients
        if len(ingredients) < 2:
            continue

        nutritions['ingredients'] = ingredients
        cam_path = choose_cam(os.path.join(img_path, item[0]))

        # Skip entries without available camera images
        if cam_path:
            result = query_openai(cam_path, nutritions)
            if result:
                res.append(result)
        
        
    return res
            
def conv_data(path):
    from multiprocessing import Pool
    final = []
    with open(path, newline='') as csvfile:
        data = list(csv.reader(csvfile, delimiter=','))
        entries = []
        for i in range(batch_size):
            entries.append((data[i::batch_size],i))
        with Pool(processes=batch_size) as pool:
            results = pool.starmap(batch_query,entries)
            print('finished')
            for i in results:
                final += i
    return final

results = []
for path in paths:
   results+=conv_data(os.path.join(root_path,path))
print(f'final data amount:{len(results)}')
import json
json.dump(results, open(os.path.join(root_path,'label.json'), 'w'))
