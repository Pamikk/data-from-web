import base64
from openai import OpenAI
import os
import pandas as pd
def read_n5k_meta(path):
  header_names = ['dish_id', 'total_calories', 'total_mass', 'total_fat', 'total_carb', 'total_protein']
  df = pd.read_csv(path,names=header_names,usecols=range(len(header_names)))
  return df
# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
def dict_to_string(data):
    res = ''
    for k,v in data.items():
        res+=f'{k}:{v},'
    return res
def get_response(img,nutritions):
  client = OpenAI()
  msg =[
    {"role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "given the info of the dish in the image,generate a conversation no more than 3 rounds that user asking LLM about the dish info for multimodal LLM finetuning",
        }]},
    {"role": "user",
        "content": [{
          "type": "text",
          "text": dict_to_string(nutritions),
        },
          {
          "type": "image_url",
          "image_url": {
            "url":  f"data:image/jpeg;base64,{img}","detail": "high"
          },
        },
      ],
    }
]
  response = client.chat.completions.create(
      model="gpt-4o",
      messages=msg,
  )
  return response.choices[0].message.content
if __name__ == '__main__':
  path = './n5k'
  data = read_n5k_meta('./n5k/dish_metadata_cafe1.csv')
  print(len(data))
  for i in os.listdir(path):
    if i.endswith('.jpeg'):
      img = encode_image(os.path.join(path,i))
      fn = i.split('_')[1]
      did = 'dish_'+fn
      print(did)
      nutritions = data[data['dish_id']==did].to_dict(orient='records')[0]
      print(nutritions)  
      print(get_response(img,nutritions))
