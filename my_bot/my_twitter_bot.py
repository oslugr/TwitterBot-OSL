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
	last_seen_id = retrieve_last_seen_id(FILE_NAME)

	#Bloque saludo
	saludo = "saludo"
	search_saludo = "@pruebarri_bot !HolaOSL"
	tweets_saludo = tweepy.Cursor(api.search, search_saludo, since_id=last_seen_id).items(numberOfTweets)

	#Bloque web
	web = "web"
	search_web = "@pruebarri_bot !web"
	tweets_web = tweepy.Cursor(api.search, search_web, since_id=last_seen_id).items(numberOfTweets)

	#Bloque de respuestas
	responder(last_seen_id,tweets_saludo,saludo)
	responder(last_seen_id,tweets_web,web)
	return



def responder(last_seen_id, tweets, tipo):
	for tweet in tweets:
		try:
			#Selecciona respuesta en función de la interacción
			if tipo == "saludo":
				phrase = random.choice(f)
			elif tipo == "web":
				phrase = "Nuestra web es https://osl.ugr.es/"
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
	return

while True:
    responder_tweets()
    time.sleep(60) #Ciclo por minuto
