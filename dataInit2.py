import json
import GetOldTweets3 as got
from langdetect import detect
import codecs
import re

f=codecs.open("D22.txt","w",encoding='utf8')
f.close()
f2=codecs.open("D12.txt","w",encoding='utf8')
f2.close()
tweet_covid_set=got.manager.TweetCriteria().setQuerySearch('#COVID-19').setSince('2020-02-01').setMaxTweets(1000)
tweets_covid=got.manager.TweetManager.getTweets(tweet_covid_set)
for idx,tweet in enumerate(tweets_covid):
	txt=str(tweet.text)
	text_edit=re.sub(r'\n','',txt)
	edited_tweet=re.sub(r'RT','',text_edit)
	with codecs.open("D22.txt","a+",encoding='utf8') as f:
		f.write(str(tweet.id)+"\t"+edited_tweet+"\n")
