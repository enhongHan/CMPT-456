import spacy
import json
import time 
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections
import nltk
from nltk.corpus import stopwords
global stop_words
stop_words=set(stopwords.words('english'))

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

def remove_stopwords(X):
	global stopwords
	words=[]
	for i in X:
		if i not in stop_words and len(i) > 2 and i!='nan':
			words.append(i)
	return words

if __name__ =="__main__":
	columns = ['id','text']
	df = pd.read_csv('D2.txt',names = columns, sep="\t",encoding="unicode_escape")
	df['tidy_tweet']=df['text'].apply(remove_url_punctuation)
	df['en'] = df['text'].apply(detect_lang)
	df = df[df['en']=='en']
	df['word_list']=df['tidy_tweet'].apply(split_words)
	df['nlp_list']=df['word_list'].apply(remove_stopwords)
	#problem 1 question 1 
	word_unique_list = (df['nlp_list'].explode()).unique()
	print(len(word_unique_list))
	#problem 1 question 2
	word_list=list(df['nlp_list'].explode())
	total_words = len(word_list)
	word_list_dict = collections.Counter(word_list)
	print(word_list_dict.most_common(10))
	normalized_count={}
	# convert to a list of (elem, cnt) pairs
	for k,v in word_list_dict.items():
		normalized_count[k] = v/total_words

	sorted(normalized_count.items(),key=lambda item:item[1])
	print(len(normalized_count.items()))
	# nltk_count=nltk.FreqDist(word_list)
	# print(nltk_count.most_common(10))
