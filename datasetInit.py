from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re
import os


access_token="4419118993-Aa9ixOtDaqi6VYdSDJRCIVWWtijLAcm5GilBGiF"
access_token_secret ="tSS8onYJPnxH1Yjakjm2e8o7EGjkpn7huT9rmaHBumMw9"
consumer_key = "GSeU8MwsVZ3DvkwYTKCKOH1Nx"
consumer_secret = "VXwDdU5TyB9ZpPRSzmHrRUEwXOQU4eoQDiCoBMK0DOGJxfcpdo"

tracklist = ['#COVID-19']
tweet_count = 0
n_tweets = 100
f=open("D2.txt","w")
f.close()

class StdOutListener(StreamListener):
	def on_data(self,data):
		global tweet_count
		global n_tweets
		global stream
		if tweet_count < n_tweets:
			try:
				data_dir=json.loads(data)
				if(data_dir["is_quote_status"]):
					tweet_count+=1
					text=data_dir["text"]
					text_edit=re.sub(r'\n','',text)
					tweet=re.sub(r'RT','',text_edit)
					with open("D2.txt","a+") as txt:
						txt.write(str(data_dir["id"]) + "\t" + tweet + "\n" )



			except BaseException:
				print("false:",tweet_count)

			return True
		else:
			stream.disconnect()

	def on_error(self,status):
		print(status)

l = StdOutListener()
auth= OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
stream = Stream(auth,l)



stream.filter(track=tracklist,is_async=True)

