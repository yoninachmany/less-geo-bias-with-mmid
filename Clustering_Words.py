#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 21:16:04 2019

@author: aditya
"""


"""
This File Takes in the following Files:
    1) Pretrained Glove Embeddings of Dimension 100
    2) The Dictionaries that Ellie Palvick created

For each of the 10 classes that we chose, this script prints out the top 20 words with highest cosine similarity to our class. We then manually 
go through each of the words and select the ones we think are correct

"""



import numpy as np
from os import listdir
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity


start = datetime.now()

def loadGloveModel(gloveFile):
    print("Loading Glove Model")
    f = open(gloveFile,'r')
    model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print("Done.",len(model)," words loaded!")
    return model



filepath = "/Users/aditya/Downloads/dictionaries/"
all_files = [filepath + a for a in listdir(filepath)]
#all_files = [a for a in all_files if ".hi" in a]
all_eng_words = []
words_num_lang = {}
for element in all_files:
    with open(element) as f:
        data = f.read().split("\n")[:-1]
        for line in data:
            line_data = line.split("\t")[1:]
            for temp in line_data:
                all_eng_words.append(temp)
                if temp in words_num_lang.keys():
                    words_num_lang[temp].append(element.split("/")[-1])
                else:
                    words_num_lang[temp] = [element.split("/")[-1]]
                    
all_eng_words = list(set(all_eng_words))
for key in words_num_lang.keys():
    words_num_lang[key] = list(set(words_num_lang[key]))


filepath = "/Users/aditya/Downloads/glove.6B.100d.txt"
model = loadGloveModel(filepath)

common_words = []
uncommon_words = []
for word in all_eng_words:
    try:
        model[word]
        common_words.append(word)
    except KeyError:
        uncommon_words.append(word)
 
    
#%%
        
similarity_word = "bride"
num_top_words = 20
        
person = np.array([model[similarity_word]])

word_similarity_score = []       
for word in common_words:
    word_embed = np.array([model[word]])
    sim_metric = cosine_similarity(person,word_embed)
    word_similarity_score.append((word,sim_metric[0][0]))
    
word_similarity_score = sorted(word_similarity_score,key = lambda x: x[1],reverse=True)
for i in range(num_top_words):
    print(word_similarity_score[i][0])

end = datetime.now()
print(end-start)


#%%

for word in all_eng_words:
    if similarity_word in word:
        print(word)
#%%
        
        
search_items = {}
with open("/Users/aditya/Classes/CIS700/Project/Classes.txt") as f:
    data = f.read().split("\n")
    for line in data:
        key = line.split(",")[0].strip()
        search = [a.strip().lower() for a in line.split(",")[1:]]
        search_items[key] = search
    


