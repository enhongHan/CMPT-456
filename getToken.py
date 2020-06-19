# import spacy
import json
import numpy as np
import re
import pandas as pd
import matplotlib.pyplot as plt
# from wordcloud import WordCloud
import collections
# from sklearn.linear_model import LinearRegression
# import nltk
import math
from nltk.corpus import stopwords
global stop_words
stop_words=set(stopwords.words('english'))

def func(x,k):
	# log(p(r))=logc-logr
	# x=logr,k=logc
	return k-x

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
def build_df(fileName):
	columns = ['id','text']
	df = pd.read_csv(fileName,names = columns, sep="\t",encoding="unicode_escape",nrows=1100)
	df['tidy_tweet']=df['text'].apply(remove_url_punctuation)
	df['en'] = df['text'].apply(detect_lang)
	df = df[df['en']=='en']
	df = df.head(1000)
	df['word_list']=df['tidy_tweet'].apply(split_words)
	df['nlp_list']=df['word_list'].apply(remove_stopwords)
	return df
def problem1question1(df1,df2,requirement):
	#	requirement decide which number user need, 
	#	if they need data with stopwords use requirement: word_list or 
	# 	they can use nlp_list
	word_unique_list1 = (df1[requirement].explode()).unique()
	word_unique_list2 = (df2[requirement].explode()).unique()
	unique_words1 = len(word_unique_list1)
	unique_words2 = len(word_unique_list2)
	return unique_words1,unique_words2

def problem1question2part1(df,requirement):
	# same as above
	word_list=list(df[requirement].explode())
	word_list_dict = collections.Counter(word_list)
	#sort word_list_dict it is same as counter.most_common()
	sorted_counter = sorted(word_list_dict.items(),key=lambda item:item[1],reverse=True)
	return sorted_counter,sorted_counter[:100]
def problem1question2part2(df1_tokens,df2_tokens):
	#change from counter to dict
	df1_tokenDict = {x[0]:x[1] for x in df1_tokens}
	df2_tokenDict = dict(df2_tokens)
	top100_list={}
	counter=0
	for x in df2_tokenDict.keys():
		if (x=='' or x==' '):
			continue
		if ((x in df1_tokenDict.keys() and df2_tokenDict[x]>df1_tokenDict[x])):
			top100_list.update({x:(df2_tokenDict[x],df1_tokenDict[x])})
			counter=counter+1
		if (counter>=100):
			return top100_list
		if ((x not in df1_tokenDict.keys())):
			top100_list.update({x:(df2_tokenDict[x],0)})
			counter=counter+1
		if (counter>=100):
			return top100_list
	return top100_list
def problem1question3(df1,num_unique1,df1_sorted_tokens,tit):
	from scipy.optimize import curve_fit
	total_words1 = len(df1['word_list'].explode())
	normalized_count1={}
	for k,v in df1_sorted_tokens:
		normalized_count1[k] = (v/total_words1)
	sorted_count=sorted(normalized_count1.items(),key=lambda item:item[1],reverse=True)
	pr_list = []
	pr_list_for_median = []
	pr_list_token = []
	for x in sorted_count:
		pr_list.append(math.log(x[1]))
		pr_list_token.append([x[0]])
		pr_list_for_median.append(round(x[1],4))
	median100 = round((np.median(pr_list_for_median[:100]))*50,4)
	median50 = round((np.median(pr_list_for_median[:50]))*25,4)
	rank_list = [math.log((x+1)) for x in range(num_unique1)]
	# regdf1=LinearRegression().fit(rank_list1[:150],pr_list[:150])
	# regdf1_inter = regdf1.intercept_
	# regdf1_coef = regdf1.coef_
	intercept,poly_cov = curve_fit(func,rank_list[:150],pr_list[:150])
	yval = func(rank_list[:150],intercept[0])
	yval2 = func(rank_list[:150],np.float64(math.log(0.1)))
	the_C = math.exp(intercept[0])
	plot1=plt.plot(rank_list[:150],pr_list[:150],'b-',label='original')
	plot2=plt.plot(rank_list[:150],yval[:150],'r+',label='polyfit')
	plot3=plt.plot(rank_list[:150],yval2[:150],'go',label='profectfit')
	plt.xlabel('logx')
	plt.ylabel('logpr')
	#set legend location
	plt.legend(loc=4)
	plt.title('curve_fit/true_poly/original'+'\t'+tit)
	plt.show()
	return median50,median100,the_C,sorted_count

if __name__ =="__main__":
	#build dataframe and get tokens, get words with/without stopwords
	df1 = build_df('D12.txt')
	df2 = build_df('D22.txt')
	


	#problem 1 question 1 
	num_unique1,num_unique2 = problem1question1(df1,df2,'word_list')
	print('Problem 1 Question 1')
	print('number of unique words df1\tdf2:',num_unique1,num_unique2)
	


	#problem 1 question 2
	df1_sorted_tokens,df1_top100_tokens = problem1question2part1(df1,'word_list')
	df2_sorted_tokens,df2_top100_tokens = problem1question2part1(df2,'word_list')
	top100_list=problem1question2part2(df1_sorted_tokens,df2_sorted_tokens)
	print('Problem 1 Question 2')
	helper=list(top100_list)
	print('top 5 of top100_list:',helper)
	


	# problem 1 question 3
	median501,median1001,the_C1,sorted_count1 = problem1question3(df1,num_unique1,df1_sorted_tokens,'dataset1')
	median502,median1002,the_C2,sorted_count2 = problem1question3(df2,num_unique2,df2_sorted_tokens,'dataset2')
	print('Problem 1 Question 3')
	print('median 50 data comparation 1\t2:',median501,median502)
	print('median 100 data comparation 1\t2:',median1001,median1002)
	print('function fit comparation 1\t2:',the_C1,the_C2)
	


	#problem 1 question 4
	sorted_count1_dict = dict(sorted_count1)
	sorted_count2_dict = dict(sorted_count2[:500])
	q4_ans_list=[]
	for x in sorted_count2_dict.keys():
		if (x=='' or x ==' '):
			continue
		if (x in sorted_count1_dict.keys() and sorted_count2_dict[x]>sorted_count1_dict[x]):
			helper1 = sorted_count1_dict[x]
			helper2 = sorted_count2_dict[x]
			q4_ans_list.append((x,(helper2-helper1)))
		elif (x not in sorted_count1_dict.keys()):
			q4_ans_list.append((x,sorted_count2_dict[x]))
	print('Problem 1 Question 4')
	print('the top 10 in question 4 answer list',q4_ans_list[:10])


# #question 4
# # 	total_occ = len(df['word_list'].explode())	
# 	# nltk_count=nltk.FreqDist(word_list)
# 	# print(nltk_count.most_common(10))
