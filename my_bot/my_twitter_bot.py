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

FILE_NAME= 'ultimo_id.txt'

def retrieve_last_seen_id(file_name):
	f_read = open(file_name, 'r')
	last_seen_id = int(f_read.read().strip())
	f_read.close()
	return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
	f_write = open(file_name, 'w')
	f_write.write(str(last_seen_id))
	f_write.close()
	return

def responder_tweets():
	search = "@pruebarri_bot HolaOSL"
	last_seen_id = retrieve_last_seen_id(FILE_NAME)
	tweets = tweepy.Cursor(api.search, search, since_id=last_seen_id).items(numberOfTweets)
    	
	for tweet in tweets:
		try:
			#Reply
			phrase =random.choice(f)
			print('\nTweet by: @' + tweet.user.screen_name)
			print('ID: @' + str(tweet.id))
			tweetId = tweet.id
			
			if tweetId > last_seen_id:
				store_last_seen_id(tweetId, FILE_NAME)
				
			username = tweet.user.screen_name
			api.update_status(phrase, in_reply_to_status_id = tweetId,auto_populate_reply_metadata=True)
			print ("Replied with " + phrase) 
		except tweepy.TweepError as e:
			print(e.reason)
		except StopIteration:
			break
                

while True:
    responder_tweets()
    time.sleep(60) #Ciclo por minuto
