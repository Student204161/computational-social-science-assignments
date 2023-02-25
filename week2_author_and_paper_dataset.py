import numpy as np
import pandas as pd
import requests
import json
import os

RESPONSE_SAVE_LOC = '/work3/s204161/'

ids_list = list(np.load(r'/zhome/a7/0/155527/Desktop/s204161/Computational-Social-Science-Exercises/week2/author_ids.npy',allow_pickle=True))


#-------------author_dataset----------------
author_dataset_dict_list = [] #[None for x in range(len(response))]
for counter, author in enumerate(response):
    paper_category_list = []
    citationCount = 0 #num times author was cited

    #this block might be superfluos if response not faulty.
    # if isinstance(author,str) == True:
    #     continue
    # elif author == None:
    #     #print(f'Entry {counter} is None.')
    #     continue
    for paper in author.get('papers'):
        None if (paper['s2FieldsOfStudy'] == []) else (paper_category_list.append(paper['s2FieldsOfStudy'][0]['category']))
        citationCount += paper['citationCount']
    #print(paper_category_list)
    author_dataset_dict = {
        'authorId': author['authorId'],
        'name': author['name'],
        'aliases': author['aliases'],
        'citationCount': citationCount,
        'field': None if paper_category_list == [] else max(set(paper_category_list), key=paper_category_list.count)

    }
    author_dataset_dict_list.append(author_dataset_dict)

author_df = pd.DataFrame(author_dataset_dict_list)
#print(author_df)


#-----------------------paper dataset----------------

paper_dataset_dict_list = [] #[None for x in range(len(response))]
paper_id_dict = {}
for counter, author in enumerate(response):
    for paper in author.get('papers'):
        if paper['paperId'] not in paper_id_dict: # Only add paper if paper not already denoted using  other author.
            paper_id_dict[paper['paperId']] = len(paper_id_dict) #  Keep track by denoting the index of each paper in the data, chronologically.

            paper_dataset_dict = {
                    'paperId': paper['paperId'],
                    'title': paper['title'],
                    'year': paper['year'],
                    'externalId.DOI': paper['externalIds'],
                    'citationCount': paper['citationCount'], #num times 
                    'authorIds': [author['authorId']] ,
                    's2FieldsOfStudy': None if (paper['s2FieldsOfStudy'] == []) else (paper['s2FieldsOfStudy'][0]['category'])
                }
            paper_dataset_dict_list.append(paper_dataset_dict)
        else:
            current_paper_index = paper_id_dict[paper['paperId']]
            paper_dataset_dict_list[current_paper_index]['authorIds'].append(author['authorId'])

paper_df = pd.DataFrame(paper_dataset_dict_list)

paper_abstract_dataset_dict_list = [] #[None for x in range(len(response))]
paper_abstract_id_dict = {}
for counter, author in enumerate(response):

    for paper in author.get('papers'):
        if paper['paperId'] not in paper_abstract_id_dict:
            paper_abstract_id_dict[paper['paperId']] = len(paper_abstract_id_dict) #  Denote the index of each paper in the data, chronologically.

            paper_abstract_dataset_dict = {
                    'paperId': paper['paperId'],
                    'abstract': paper['abstract'],

                    # 's2FieldsOfStudy': None if (paper['s2FieldsOfStudy'] == []) else (paper['s2FieldsOfStudy'][0]['category'])
                }
            paper_abstract_dataset_dict_list.append(paper_abstract_dataset_dict)


paper_abstract_df = pd.DataFrame(paper_abstract_dataset_dict_list)

#print(paper_df)

author_df.to_csv(r'/work3/s204161/author_df.csv')
paper_df.to_csv(r'/work3/s204161/paper_df.csv')
paper_abstract_df.to_csv(r'/work3/s204161/paper_astract_df.csv')

