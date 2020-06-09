import spacy
import json
import time 
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections


def remove_url_punctuation(X):
	url_pattern = re.compile(r'https?://\S+|www\.\S+')
	replace_url = url_pattern.sub(r'',str(X))
	punct_pattern = re.compile(r'[^\w\s]')
	no_punct = punct_pattern.sub(r'',replace_url).lower()
	return no_punct
def detect_lang(X):
	from langdetect import detect
	try:
		lang=detect(X)
		return (lang)
	except:
		return("other")
def split_words(X):
	split_word_list = X.split(" ")
	return split_word_list

columns = ['id','text']
df = pd.read_csv('D2.txt',names = columns, sep="\t",encoding="unicode_escape")
df['tidy_tweet']=df['text'].apply(remove_url_punctuation)
df['en'] = df['text'].apply(detect_lang)
#对整个df进行整体约束
df = df[df['en']=='en']
print(df.head())
