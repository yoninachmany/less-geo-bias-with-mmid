#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 22:52:55 2019

@author: aditya
"""

import pandas as pd
import ast
from distutils.dir_util import copy_tree
import os

"""
This file takes as input:
    1) csv file that Yoni created where the paths for each word,language are given. (ids.csv)
    2) Original MMID dataset
    3) List of Classes and synonyms that we selected (Classes.txt)

Output:
    1) Outputs the Data-set that we use for our analysis

"""



#considered_languages = ["Unnamed: 0","bn","bpy","gu","hi","kn","ml","mr","pa","ta","te"]
considered_languages = ["Unnamed: 0"]
for i in range(2,28):
    if i < 10:
        considered_languages.append("english-0" + str(i))
    else:
        considered_languages.append("english-" + str(i))



#files = ["scale-bengali-package","scale-bishnupriya-manipuri-package","scale-gujarati-package","scale-hindi-package","scale-kannada-package","scale-malayalam-package","scale-marathi-package","scale-punjabi-package","scale-tamil-package","scale-telugu-package"]
files = []
for i in range(2,28):
    if i < 10:
        files.append("scale-english-0" + str(i) + "-package")
    else:
        files.append("scale-english-" + str(i) + "-package")


files = ["/nlp/data/MMID/raw/" + a + "/" for a in files]

code_path_dict = {}
for i in range(1,len(considered_languages)):
    code_path_dict[considered_languages[i]] = files[i-1]

data = pd.read_csv("ids_corrected.csv").fillna("N/A")

data = data[considered_languages]


synonym_path_dict = {}
for index,row in data.iterrows():
    word = row["Unnamed: 0"].lower()
    for lan in considered_languages[1:]:
        temp_path = row[lan]
        if temp_path != "N/A" and word in synonym_path_dict.keys():
            synonym_path_dict[word].append([code_path_dict[lan] + str(a) for a in ast.literal_eval(temp_path)])
        elif temp_path != "N/A" and word not in synonym_path_dict.keys():
            synonym_path_dict[word] = [[code_path_dict[lan] + str(a) for a in ast.literal_eval(temp_path)]]

for key in synonym_path_dict.keys():
    synonym_path_dict[key] = [item for sublist in synonym_path_dict[key] for item in sublist]


intermediate_1 = {}

for key in synonym_path_dict.keys():
    intermediate_1[key] = {}
    list_of_paths = synonym_path_dict[key]
    path_to_language = {a:"-".join(a.split("/")[-2].split("-")[1:-1]) for a in list_of_paths}
    for path,language in zip(path_to_language.keys(),path_to_language.values()):
        if language in intermediate_1[key].keys():
            intermediate_1[key][language].append(path)
        else:
            intermediate_1[key][language] = [path]

        
search_items = {}
with open("Classes.txt") as f:
   data = f.read().split("\n")
   for line in data:
       key = line.split(",")[0].strip()
       search = [a.strip().lower() for a in line.split(",")[1:]]
       search_items[key.lower()] = search
            
search_tree = {}
for key in search_items.keys():
    synonyms = search_items[key]
    search_tree[key] = {}
    for element in synonyms:
        if element in intermediate_1.keys():
            search_tree[key][element] = intermediate_1[element]

for i in range(5):
    for key in search_tree.keys():
        if len(search_tree[key]) == 0:
            del search_tree[key]
            break

master_save_path = "/nlp/data/kashyap/DeepLearning/Data_Eng/"


lookup_to_save = {}
for word in search_tree.keys():
    for synonym in search_tree[word].keys():
        for language in search_tree[word][synonym].keys():
            for lookup_path in search_tree[word][synonym][language]:
                save_path = master_save_path + word + "/" + synonym + "/" + language + "/" + lookup_path.split("/")[-1]
                lookup_to_save[lookup_path] = save_path

for lookup_path in lookup_to_save.keys():
    save_file = lookup_to_save[lookup_path]
    save_file_folders = save_file.replace(master_save_path,"").split("/")
    temp_path = master_save_path
    for folder in save_file_folders:
        temp_path += folder + "/"
        if not os.path.isdir(temp_path):
            os.mkdir(temp_path)

for lookup_path in lookup_to_save.keys():
    save_path = lookup_to_save[lookup_path]
    try:
        copy_tree(lookup_path, save_path)    
    except:
        pass
    
    
