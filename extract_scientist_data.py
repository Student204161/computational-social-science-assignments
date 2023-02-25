import numpy as np
import pandas as pd
import requests
import json
import os
RESPONSE_SAVE_LOC = '/work3/s204161'
ids_list = list(np.load(r'/zhome/a7/0/155527/Desktop/s204161/Computational-Social-Science-Exercises/week2/author_ids.npy',allow_pickle=True))

#Uses checkpoints in case connection to server is unstable.
if os.path.exists(fr'{RESPONSE_SAVE_LOC}/response.json'):
    with open(fr'{RESPONSE_SAVE_LOC}/response.json', "r") as f:
        # Load the contents of the file into a Python list
        response = json.load(f)
    response_items = []
    for item in response:
        if isinstance(item,dict):
            response_items.append(item)
    logged_ids = [ x['authorId'] for x in response_items]
else: response, logged_ids = [], []

ids_list = [int(x) for x in ids_list if (isinstance(x,str) or isinstance(x,int))]
remaining_ids = set(ids_list) - set(logged_ids)

BASE_URL = 'https://api.semanticscholar.org/graph/'
VERSION = 'v1/'
RESOURCE = 'author/batch'
CHUNK_SIZE = 100

COMPLETE_URL = BASE_URL + VERSION + RESOURCE

#When we have to send data ind, we use requests.post() and max author request size is 100 at a time.
params = {"fields": [
    "name,aliases,papers,papers.title,papers.abstract,papers.year,papers.externalIds,papers.s2FieldsOfStudy,papers.citationCount"]
}
print(f'Retrieving data, num requests:{len(remaining_ids)}')
for i in range(0, int(len(remaining_ids)), CHUNK_SIZE): # len(ids_list)
    idsx = remaining_ids[i:i + CHUNK_SIZE]
    idsx_json = {"ids" : idsx}
    responsex = requests.post(COMPLETE_URL, json=idsx_json, params=params).json()
    response += responsex
    print(f'{i+CHUNK_SIZE} requests')

print('Data retrieved')

json_string = json.dumps(response)

with open(fr'{RESPONSE_SAVE_LOC}/response.json', "a") as f:
    f.write(json_string)

print(fr'RESPONSE saved to path:{RESPONSE_SAVE_LOC}/response.json')

