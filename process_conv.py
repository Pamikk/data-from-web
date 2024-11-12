import json
import os
import csv
root_path = '/home/dataset/nutrition5k_dataset'
mis_img = 0
single = 0
def filter_data(filter_ids,data):
    filter_ids = filter_ids[::-1]
    data = data[::-1]
    for j,item in enumerate(data):
        flag = False
        for i,id in enumerate(filter_ids):
            if id in item['image'][0]:
                filter_ids.pop(i)
                flag = True
                break
        if flag:
            data.pop(j)
        if not filter_ids:
            break
    return data
with open(os.path.join(root_path,'label.json'),'r') as f:
    data = json.load(f)
    processed = []
    for item in data:
        if not os.path.exists(item['image'][0]):
            mis_img +=1
        if len(item['history']) == 0:
            single+=1
        if 'calor' in item['query'] or 'Calor' in item['query']:
            processed.append(item)
            continue
        history = []
        for q,a in item['history']:
            if 'calor' in q or 'Calor' in q:
                item['query'] = q
                item['response'] = a
                break
            else:
                history.append([q,a])
        item['history'] = history
        processed.append(item)
with open(os.path.join(root_path,'metadata/dish_metadata_cafe2.csv'),'r') as f:
    data = list(csv.reader(f, delimiter=','))
    ids = [item[0] for item in data]
    #print(len(ids))
    processed = filter_data(ids,processed)
    print(single,mis_img)
    #print(len(processed))
    #json.dump(processed,open(os.path.join(root_path,'newlabel.json'),'w'))
    
