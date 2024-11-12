import base64
from openai import OpenAI
import os
from httpx import HTTPStatusError
def read_n5k_meta(path):
  import pandas as pd
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
import time
def process_results(results):
    if results == None:
        return []
    results = results.split('\n')
    final = []
    for i in results:
        i = i.strip()
        i = i.strip('-')
        if len(i)>2:
            final.append(i)
    return final
def get_response(img,nutritions):
  client = OpenAI()
  msg =[
    {"role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "given the info of the dish in the image,generate a QA conversation no more than 3 rounds that user asking LLM about the dish info for multimodal LLM finetuning,odd line is user questioning and even line for assistant answers, don't add additional info must include calories, make the numbers look more natrual",
        }]},
    {"role": "user",
        "content": [{
          "type": "text",
          "text": dict_to_string(nutritions),
        },
          {
          "type": "image_url",
          "image_url": {
            "url":  f"data:image/jpeg;base64,{img}",
          },
        },
      ],
    }
]
  sleep_time = 5
  for _ in range(0,5):  # try 4 times
      try:
          response = client.chat.completions.create(
              model="gpt-4o",
              messages=msg,
          )
          #time.sleep(1.2)
          response = process_results(response.choices[0].message.content)
          str_error = None
          if len(response)<2:
             str_error = 'retry'
      except Exception as e:
        str_error = str(e)
      if str_error:
         if not (str_error == 'retry'):
             time.sleep(sleep_time)
      else:
        break
  return response
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
