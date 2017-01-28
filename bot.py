# -*- coding: utf-8 -*-
import re

# Bot base modules
from telegram.ext import Updater, CommandHandler

# Message Handler Setup
from telegram.ext import MessageHandler, Filters

# Set up updater and dispatcher
TOKEN = open("token.txt", "r").read()
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# Logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Lista de Usuarios

user_set = set()

# Filtros
def keywords(mensaje_str):
	msg = str(mensaje_str)
	if re.compile(r"moci(o|ó)?n(es)? de (procedimiento)s?", re.IGNORECASE).search(msg):
		return open("mociones/mocion_procedimiento.txt", "r").read()
	
	elif re.compile(r"moci(o|ó)?n(es)? de (ó|o)?rden(es)?", re.IGNORECASE).search(msg):
		return open("mociones/mocion_orden.txt", "r").read()
	
	elif re.compile(r"moci(o|ó)?n(es)? de duda(s)?", re.IGNORECASE).search(msg):
		return open("mociones/mocion_duda.txt", "r").read()
	
	elif re.compile(r"caucus simple(s)?", re.IGNORECASE).search(msg):
		return open("caucus/simple.txt", "r").read()
	
	elif re.compile(r"caucus moderado(s)?", re.IGNORECASE).search(msg):
		return open("caucus/moderado.txt", "r").read()
	
	elif re.compile(r"caucus(es)?", re.IGNORECASE).search(msg):
		return open("caucus/index.txt", "r").read()
	
	elif re.compile(r"anteproyectos?", re.IGNORECASE).search(msg):
		return open("anteproyecto/index.txt", "r").read()
	
	elif re.compile(r"debate(s)?( particular(es)?)?( de anteproyectos?)?", re.IGNORECASE).search(msg):
		return open("debate_particular/index.txt", "r").read()
		
	elif re.compile(r"defender (el|los) anteproyectos?", re.IGNORECASE).search(msg):
		return open("debate_particular/index.txt", "r").read()
	
	else:
		return "_*ERROR*_\n\nNo se han encontrado resultados de búsqueda para <`{}`> 😕\n\nSi necesitas ejecutar un comando usa /help para ver la lista.".format(mensaje_str)

		
# ----------------------------------------- Commands -----------------------------------------

# Bienvenida
def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=open("welcome.txt", "r").read(), parse_mode="Markdown")
	user_set.add(update.message.chat_id)
	user_list = str(user_set)
	bot.sendMessage(chat_id=update.message.chat_id, text="IDs de usuarios en línea:\n" + user_list)
	
# Manual

def manual(bot, update):
	manual_pdf = open("manual.pdf")
	bot.sendDocument(chat_id=update.message.chat_id, document=manual_pdf)
	

# Comando Desconocido
def unknown(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Lo siento, no reconozco ese comando 😕")
	
	
# Búsqueda
def request_info(bot, update):
	msg = update.message.text
	response = str(keywords(msg))
	bot.sendMessage(chat_id=update.message.chat_id, text=response, parse_mode="Markdown")
	
	
# --------------------------------------------------------------------------------------------
	
# Command Handlers
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
manual_handler = CommandHandler('manual', manual)
dispatcher.add_handler(manual_handler)
ayuda_handler = CommandHandler('ayuda', start)
dispatcher.add_handler(ayuda_handler)


# Message Handlers
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

query_handler = MessageHandler(Filters.text, request_info)
dispatcher.add_handler(query_handler)


updater.start_polling()
updater.idle()