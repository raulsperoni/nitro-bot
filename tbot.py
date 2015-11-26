#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import requests
import json

usuarios = {}

bot = telebot.TeleBot("TOKEN")

def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None

def in_storage(unique_code): 
    # Should check if a unique code exists in storage
    return get_username_from_storage(unique_code) is not None

def get_username_from_storage(unique_code): 
    # Does a query to the storage, retrieving the associated username
    response = requests.get('http://localhost:8080/nitro-ws/rest/votantes/'+unique_code)
    assert response.status_code == 200
    return response.json()["nombre"]

def save_chat_id(chat_id, unique_code, username):
    # Save the chat_id->token to storage
    response = requests.post('http://localhost:8080/nitro-ws/rest/votantes/'+unique_code+'/'+str(chat_id))
    usuarios[chat_id]=(username,unique_code)

def get_votaciones(chat_id, unique_code):
    response = requests.get('http://localhost:8080/nitro-ws/rest/votacion/'+unique_code+'/'+str(chat_id))
    print response.json()
    return "Pregunta 1 - \n"+response.json()[0]["pregunta"]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    unique_code = extract_unique_code(message.text)
    if unique_code: # if the '/start' command contains a unique_code
        username = get_username_from_storage(unique_code)
        if username: # if the username exists in our database
            save_chat_id(message.chat.id, unique_code,username)
            reply = "Hola {0}, como estás?".format(username)
        else:
            reply = "No se quién sos..."
    else:
        reply = "Tenés que visitarme usando el link"
    bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['ver'])
def send_welcome(message):
    usr = usuarios.get(message.chat.id,None)
    if usr is None:
	procesar_todos(message)
    else:
	reply = get_votaciones(message.chat.id, usr[1])
    	bot.send_message(message.chat.id, reply)

@bot.message_handler(func=lambda m: True)
def procesar_todos(message):
    print message.text
    if usuarios.get(message.chat.id,None) is None:
    	bot.send_message(message.chat.id, "Tenemos que identificarte, click en el link: https://telegram.me/chap_go_bot?start=token")
    else:
	bot.send_message(message.chat.id, "{0}, no hay votaciones activas".format(usuarios[message.chat.id][0]))

bot.polling()
