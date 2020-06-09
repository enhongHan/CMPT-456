import json
import GetOldTweets3 as got
from langdetect import detect
import codecs
import re

f=codecs.open("D12.txt","w",encoding='utf8')
f.close()
#for the getoldtweets it must search something to get result so I use 'a' here which is has high freq in english
tweet_Nohashtag_set = got.manager.TweetCriteria().setQuerySearch('a').setSince('2020-02-01').setMaxTweets(1000)
tweets_Nohashtag = got.manager.TweetManager.getTweets(tweet_Nohashtag_set)
for idx, tweet2 in enumerate(tweets_Nohashtag):
	txt=str(tweet2.text)
	text_edit=re.sub(r'\n','',txt)
	edited_tweet=re.sub(r'RT','',text_edit)
	with codecs.open("D12.txt","a+",encoding='utf8') as f:
		f.write(str(tweet2.id)+"\t"+edited_tweet+"\n")