import tweepy, time, sys, random


CONSUMER_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
CONSUMER_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
ACCESS_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

user = api.me()
print(user.name)
print(user.location)

filename=open("ejemplo.txt",'r')
f=filename.readlines()
filename.close()
numberOfTweets =10
while True:
	#for line in f:
	#   api.update_status(line)
	#  time.sleep(40)#Tweet every 15 minutes
	    
	search = "#HolaOSL"
    
	for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
		try:
			#Reply
                	phrase =random.choice(f)
                	print('\nTweet by: @' + tweet.user.screen_name)
                	print('ID: @' + str(tweet.user.id))
                	tweetId = tweet.user.id
                	username = tweet.user.screen_name
                	api.update_status(phrase, in_reply_to_status_id = tweetId)
                	print ("Replied with " + phrase) 
		except tweepy.TweepError as e:
                	print(e.reason)
		except StopIteration:
			break
                
	time.sleep(60)#Tweet every 15 minutes
