#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot

usuarios = {"a1":"raul"}
ids = {}

bot = telebot.TeleBot("112649113:AAF8Dsh2prTQZ-6Z13VCr4ELSWjoreckP-4")

def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None

def in_storage(unique_code): 
    # Should check if a unique code exists in storage
    return usuarios[unique_code]

def get_username_from_storage(unique_code): 
    # Does a query to the storage, retrieving the associated username
    # Should be replaced by a real database-lookup.
    return usuarios[unique_code] if in_storage(unique_code) else None

def save_chat_id(chat_id, username):
    # Save the chat_id->username to storage
    # Should be replaced by a real database query.
    ids[chat_id]=username

@bot.message_handler(commands=['start'])
def send_welcome(message):
    unique_code = extract_unique_code(message.text)
    if unique_code: # if the '/start' command contains a unique_code
        username = get_username_from_storage(unique_code)
        if username: # if the username exists in our database
            save_chat_id(message.chat.id, username)
            reply = "Hola {0}, como estás?".format(username)
        else:
            reply = "No se quién sos..."
    else:
        reply = "Tenés que visitarme usando el link"
    bot.reply_to(message, reply)

@bot.message_handler(func=lambda m: True)
def procesar_todos(message):
    print message.text
    if ids.get(message.chat.id,None) is None:
    	bot.send_message(message.chat.id, "Tenemos que identificarte, click en el link: https://telegram.me/chap_go_bot?start=a1")
    else:
	bot.send_message(message.chat.id, "{0}, no hay votaciones activas".format(ids[message.chat.id]))

bot.polling()
