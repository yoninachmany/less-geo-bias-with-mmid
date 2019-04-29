# less-geo-bias-with-mmid
CIS 700-004: Deep Learning for Data Science final project




**Creating_Dataset.py**

This file takes as input:
    1) csv file where the paths for each word,language are given. (ids_corrected.csv)
    2) Original MMID dataset
    3) List of Classes and synonyms that we selected (Classes.txt)

Output:
    1) Outputs the Data-set that we use for our analysis


**Clustering_Words.py**

This file Takes in the following Files:
    1) Pretrained Glove Embeddings of Dimension 100
    2) The Dictionaries that Ellie Palvick created

For each of the 6 classes that we chose, this script prints out the top 20 words with highest cosine similarity to our class. We then manually 
go through each of the words and select the ones we think are correct



**IDs_of_MMID_data_to_download.ipynb**

This file downloads language traslation dictionaries obtained from Ellie Pavlicks website (https://cs.brown.edu/people/epavlick/data.html)
It outputs a mapping of a word and a language to the MMID path where the pictures exist for that word, language (our_langs_ids.csv)


**Model.ipynb**

This file takes in the Cleaned MMID dataset for the selected languages and classes and builds and evaluates the following models:
1) Logistic Regression Model
2) Convolutional Neural Network
3) Pre-trained Resnet

Metrics evaluated in these files:
1) Test Accuracy
2) Confusion Matrix






