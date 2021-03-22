import tweepy
import time
import sys
import random
import datetime as dt
import requests
import os
from bs4 import BeautifulSoup
from settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

user = api.me()
print(user.name)
print(user.location)

filename = open("ejemplo.txt", 'r')
f = filename.readlines()
filename.close()

filename = open("chistes.txt", 'r')
chistes = filename.readlines()
filename.close()

numeroTweets = 10

archivoId = 'ultimo_id.txt'
URL = "https://osl.ugr.es/"

#Función que hace scraping en la web de la OSL para obtener los datos de las últimas entradas
def scraping_osl():
    pagina = requests.get(URL)

    soup = BeautifulSoup(pagina.content, "html.parser")
    resultados = soup.find(class_="art-layout-cell art-content clearfix")
    respuesta = "Aquí te dejo los últimos posts del blog:"

    articulos = resultados.find_all("h2", class_="art-postheader")[:2]
    for articulo in articulos:
        titulo = articulo.find("a")
        if None in (titulo):
            continue
        respuesta += ' "' + str(titulo.text.strip()) + '" ' + str(titulo["href"])
    return respuesta


# Devuelve el último id visto en el archivo ultimo_id.txt
def devuelve_ultimoId(archivoId):
    f_read = open(archivoId, 'r')
    ultimoId = int(f_read.read().strip())
    f_read.close()
    return ultimoId


# Guarda el último id visto en el archivo ultimo_id.txt
def guarda_ultimoId(ultimoId, archivoId):
    f_write = open(archivoId, 'w')
    f_write.write(str(ultimoId))
    f_write.close()
    return

def generar_avatar(nombre):
    respuesta = 'python3 gen.py 120 '
    respuesta += str(nombre)
    os.system(respuesta)
    return

def responder_con_imagen(tweets):
    ultimoId = devuelve_ultimoId(archivoId)
    for tweet in tweets:
        if not tweet.retweeted and 'RT @' not in tweet.text:
            try:
                media = "./img/example.png"
                texto = "Aquí está tu avatar generado por tu nombre: "
                generar_avatar(tweet.user.screen_name)
                print('\nTweet de: @' + tweet.user.screen_name)
                print('ID: @' + str(tweet.id))
                tweetId = tweet.id
                if tweetId > ultimoId:
                    guarda_ultimoId(tweetId, archivoId)
                usuario = tweet.user.screen_name
                api.update_with_media(media, status=texto, in_reply_to_status_id=tweetId,
                                  auto_populate_reply_metadata=True)
                print("Respuesta: " + texto)
            except tweepy.TweepError as e:
                print(e.reason)
            except StopIteration:
                break
    return
# Función responsablde de elegir y realizar una respuesta
def responder(tweets, tipo):
    # La variable debe ser renovada para no repetir respuestas a tweets
    ultimoId = devuelve_ultimoId(archivoId)
    for tweet in tweets:
        if not tweet.retweeted and 'RT @' not in tweet.text:
            try:
                # Selecciona respuesta en función de la interacción
                if tipo == "saludo":
                    texto = random.choice(f)
                elif tipo == "web":
                    texto = "Nuestra web es https://osl.ugr.es/"
                elif tipo == "actividad":
                    texto = scraping_osl()
                elif tipo == "contacto":
                    texto = "Contacta con nosotros por teléfono -> 958 24 10 00 o por e-mail -> osl@ugr.es . Síguenos en nuestro Twitter para mantenerte informado sobre todo @OSLUGR "
                elif tipo == "redes":
                    texto = "Twitter: @OSLUGR Facebook: https://www.facebook.com/SoftwareLibreUGR Instagram: https://www.instagram.com/oslugr YouTube: https://www.youtube.com/user/oslugr GitHub: https://github.com/oslugr Meetup: https://www.meetup.com/es-ES/Granada-Geek Telegram: https://telegram.me/oslugr"
                elif tipo == "chiste":
                    texto = random.choice(chistes)
                elif tipo == "creador":
                    texto = "Mi padre es @Juan_Barrilao @Juan__Barri y me debe unas piernas"

                print('\nTweet de: @' + tweet.user.screen_name)
                print('ID: @' + str(tweet.id))
                tweetId = tweet.id

                if tweetId > ultimoId:
                    guarda_ultimoId(tweetId, archivoId)

                usuario = tweet.user.screen_name
                api.update_status(texto, in_reply_to_status_id=tweetId,
                                  auto_populate_reply_metadata=True)
                print("Respuesta: " + texto)
            except tweepy.TweepError as e:
                print(e.reason)
            except StopIteration:
                break
    return


# Función que detecta el tipo de tweet para luego poder responder de una manera u otra
def responder_tweets():
    ultimoId = devuelve_ultimoId(archivoId)

    # Bloque saludo
    saludo = "saludo"
    buscar_saludo = "@pruebarri_bot #hola"
    tweets_saludo = tweepy.Cursor(
        api.search, buscar_saludo, since_id=ultimoId).items(numeroTweets)

    # Bloque web
    web = "web"
    buscar_web = "@pruebarri_bot #web"
    tweets_web = tweepy.Cursor(
        api.search, buscar_web, since_id=ultimoId).items(numeroTweets)

    # Bloque actividad
    actividad = "actividad"
    buscar_actividad = "@pruebarri_bot #actividad"
    tweets_actividad = tweepy.Cursor(
        api.search, buscar_actividad, since_id=ultimoId).items(numeroTweets)

    # Bloque contacto
    contacto = "contacto"
    buscar_contacto = "@pruebarri_bot #contacto"
    tweets_contacto = tweepy.Cursor(
        api.search, buscar_contacto, since_id=ultimoId).items(numeroTweets)

    # Bloque redes
    redes = "redes"
    buscar_redes = "@pruebarri_bot #redes"
    tweets_redes = tweepy.Cursor(
        api.search, buscar_redes, since_id=ultimoId).items(numeroTweets)

    # Bloque avatar
    buscar_avatar = "@pruebarri_bot #avatar"
    tweets_avatar = tweepy.Cursor(
        api.search, buscar_avatar, since_id=ultimoId).items(numeroTweets)

    # Bloque chiste
    chiste = "chiste"
    buscar_chiste = "@pruebarri_bot #chiste"
    tweets_chiste = tweepy.Cursor(
        api.search, buscar_chiste, since_id=ultimoId).items(numeroTweets)

    # Bloque creador
    creador = "creador"
    buscar_creador = "@pruebarri_bot #creador"
    tweets_creador = tweepy.Cursor(
        api.search, buscar_creador, since_id=ultimoId).items(numeroTweets)

    # Bloque de respuestas
    responder(tweets_saludo, saludo)
    responder(tweets_web, web)
    responder(tweets_actividad, actividad)
    responder(tweets_contacto, contacto)
    responder(tweets_redes, redes)
    responder_con_imagen(tweets_avatar)
    responder(tweets_chiste, chiste)
    responder(tweets_creador, creador)
    return

# Función que responde con la última entrada del blog de la OSL
def buenos_dias():
        pagina = requests.get(URL)

        soup = BeautifulSoup(pagina.content, "html.parser")
        resultados = soup.find(class_="art-layout-cell art-content clearfix")
        respuesta = "Buenas tardes a todos, aquí os dejo la última entrada en la web de la @OSLUGR: "

        articulo = resultados.find_all("h2", class_="art-postheader")[:1]

        titulo = articulo[0].find("a")
        respuesta += ' "' + str(titulo.text.strip()) + '" ' + str(titulo["href"])
        api.update_status(respuesta)
        print("Mensaje de buenas tardes: " + respuesta)
        return



# main
while True:
    responder_tweets()
    if dt.datetime.now().hour == 3 and dt.datetime.now().minute == 0: #Mensaje programado para las 3 de la tarde
        buenos_dias()
    time.sleep(60)  # Ciclo por minuto
