#!/usr/bin/env python
# coding: utf-8

# In[2]:


# from google.colab import drive
# drive.mount('/content/drive')


# In[3]:


from joblib import load, dump
from tqdm import tqdm
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
import nltk

nltk.download("stopwords")
stopword = set(stopwords.words("english"))
nltk.download("wordnet")
from nltk.stem import WordNetLemmatizer


# In[4]:


# vec = load("/content/drive/MyDrive/hotel_recommendation/data/tfidf_vector.joblib")
# lr = load("/content/drive/MyDrive/hotel_recommendation/data/trained_model.joblib")
vec = load("./ML/files/tfidf_vector.joblib")
lr = load("./ML/files/trained_model.joblib")


# In[5]:


# prediction_data = pd.read_csv("/content/drive/MyDrive/hotel_recommendation/data/new_dataset.csv")
prediction_data = pd.read_csv(
    "./ML/files/dataset/dataset_finale.tsv", sep="\t", encoding="latin-1"
)
prediction_data.head()

import pickle

with open("./ML/files/cleaned_dataset.pkl", "rb") as f:
    clean_data_test_data = pickle.load(f)

# In[6]:


prediction_data["Hotel Location"].value_counts()


# In[7]:


prediction_data.columns


# In[8]:


lemmatizer = WordNetLemmatizer()


def data_cleaner(data):
    clean_data = []
    for sentence in tqdm(data):
        cleantext = BeautifulSoup(sentence, "lxml").text  # html tags
        cleantext = re.sub(r"[^\w\s]", "", cleantext)  # punctuation
        cleantext = [
            token for token in cleantext.lower().split() if token not in stopword
        ]  # stopword
        clean_text = " ".join([lemmatizer.lemmatize(token) for token in cleantext])
        clean_data.append(clean_text.strip())
    return clean_data


prediction_data = prediction_data.drop_duplicates(subset=["ReviewId"])
prediction_data = prediction_data.dropna(subset=["ReviewText"])
# clean_data_test_data = data_cleaner(prediction_data.ReviewText.values)


prediction_data["clean_data"] = clean_data_test_data
test_x_tfidf = vec.transform(clean_data_test_data)
predict = lr.predict(test_x_tfidf)

prediction_data["sentiment"] = predict
prediction_data["UserLocation"] = prediction_data.UserLocation.str.lower()
prediction_data["Hotel Location"] = prediction_data["Hotel Location"].str.lower()
prediction_data = prediction_data.drop(
    columns=[
        "Unnamed: 16",
        "Unnamed: 17",
        "Unnamed: 18",
        "Unnamed: 19",
        "Unnamed: 20",
        "Unnamed: 21",
        "Unnamed: 22",
        "Unnamed: 23",
        "Unnamed: 24",
        "Unnamed: 25",
        "Unnamed: 26",
        "Unnamed: 27",
        "Unnamed: 28",
        "Unnamed: 29",
        "Unnamed: 30",
        "Unnamed: 31",
        "Unnamed: 32",
        "Unnamed: 33",
        "Unnamed: 34",
        "Unnamed: 35",
        "Unnamed: 36",
        "Unnamed: 37",
        "Unnamed: 38",
        "Unnamed: 39",
        "Unnamed: 40",
        "Unnamed: 41",
    ]
)


# In[9]:


# ["users requirement text data"] ["Location"]
# ["Review Text"] [1] ["Locaiton"]


# userreq-[0.104, 0.343, 4.879, 6.343]

# 50k

# Location - UK

# 50k {UK} - 100 hotels

# checking for postive sentimented data

# hotels - 50 hotels


# vecrized -
# hotel 3 -[0.134, 1.343, 3.879, 3.343] - ecu - [0.104, 0.343, 4.879, 6.343] = 0.3
# [0.134, 4.343, 3.879, 3.343] - ecu - [0.104, 0.343, 4.879, 6.343] = 0.9
# hotel 2 -[0.134, 9.343, 3.879, 3.343] - ecu - [0.104, 0.343, 4.879, 6.343] = 0.2
# hotel 1 - [0.134, 1.333, 3.879, 3.343] - ecu - [0.104, 0.343, 4.879, 6.343] = 0.1


# ...50 hotels


# In[22]:


from scipy.spatial import distance


def compare(vec, query):
    dist = distance.euclidean(vec, query)
    return dist


def similarity(data, text, top_n=3):
    start_point = 0
    batch_point = 10
    final_df = pd.DataFrame()
    for i in range(data.shape[0]):
        new_data = data.iloc[start_point:batch_point].copy()
        if new_data.shape[0] != 0:
            arr = vec.transform(new_data.clean_data).toarray()
            query = vec.transform([text]).toarray()
            list_ = [compare(arr[i], query) for i in range(new_data.shape[0])]
            new_data["dist"] = list_
            final_df = final_df.append(new_data, ignore_index=True)
            start_point = start_point + 10
            batch_point = batch_point + 10
    final_df = final_df.sort_values(by=["dist"])
    return final_df[:top_n]


def recommendation(location, text, top_n=3):
    location = location.lower()
    text = text.lower()
    location_found = prediction_data[
        (prediction_data["Hotel Location"] == location)
    ].reset_index(drop=True)
    if location_found.empty:
        # print('Sorry we are unable to find hotels in {}'.format(location))
        return
    else:
        location_found_positive = location_found[
            location_found.sentiment == 1
        ].reset_index(drop=True)
        location_found_negative = location_found[
            location_found.sentiment == -1
        ].reset_index(drop=True)
        if location_found_positive.empty:
            # print('Sorry we are unable to find hotels in positively reviewed hotel. If you still want to proceed type yes else no')
            return
            # user_input = input()
            # if user_input == "yes":
            #   text_similar_hotel = similarity(location_found_negative,text, top_n)
            #   # return print("These are some hotels we found for your :",set(list(text_similar_hotel.HotelName)))
            #   return
            # else:
            #   print('Thank you ...see you soon')
        else:
            text_similar_hotel = similarity(location_found_positive, text, top_n)
            # return print("we think this hotels might suit you :",set(list(text_similar_hotel.HotelName)))
            return list(set(text_similar_hotel.HotelName))


# In[23]:

# recommendation("pisa, italy", "business trip", 1)
# print(recommendation("vancouver, canada","business trip"))


# In[24]:

# from pprint import pprint

# pprint(recommendation("calabria, italy","business trip", 10))
# pprint(recommendation("calabria, italy","value", 10))
# pprint(recommendation("calabria, italy","sleep", 10))
# pprint(recommendation("calabria, italy","room", 10))


print(recommendation("pisa, italy", "business trip", 7))


# In[25]:


# recommendation("mexico city, mexico","business trip", 4)


# In[ ]:


# In[ ]:


# #### Recommendation system for every hotel

# In[35]:


# all_hotel_location = prediction_data["Hotel Location"].nunique()


# In[38]:


# for each_hotel in list(prediction_data["Hotel Location"].unique()):
# print(f"Getting Location for {each_hotel}")
# recommendation(each_hotel,"business trip", 2)
# print("")


# In[ ]:
