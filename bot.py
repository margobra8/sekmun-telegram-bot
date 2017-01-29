# -*- coding: utf-8 -*-
import re
import time
from datetime import datetime

# Bot base modules
from telegram.ext import Updater, CommandHandler

# Message Handler Setup
from telegram.ext import MessageHandler, Filters
from telegram.chataction import ChatAction

# Set up updater and dispatcher
from config import TOKEN
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# Logging
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

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
	
	elif re.compile(r"moci(o|ó)?n(es)?", re.IGNORECASE).search(msg):
		return open("mociones/mociones.txt", "r").read()
	
	elif re.compile(r"caucus simple(s)?", re.IGNORECASE).search(msg):
		return open("caucus/simple.txt", "r").read()
	
	elif re.compile(r"caucus moderado(s)?", re.IGNORECASE).search(msg):
		return open("caucus/moderado.txt", "r").read()
	
	elif re.compile(r"caucus(es)?", re.IGNORECASE).search(msg):
		return open("caucus/index.txt", "r").read()
	
	elif re.compile(r"debate(s)?( particular(es)?)?( de anteproyectos?)?", re.IGNORECASE).search(msg):
		return open("debate_particular/index.txt", "r").read()
		
	elif re.compile(r"defender (el|los)? anteproyectos?", re.IGNORECASE).search(msg):
		return open("debate_particular/index.txt", "r").read()
	
	elif re.compile(r"anteproyectos?", re.IGNORECASE).search(msg):
		return open("anteproyecto/index.txt", "r").read()
	
	else:
		return "❌ _*ERROR*_\n\nNo se han encontrado resultados de búsqueda para \n<`{}`> 😕\n\nSi necesitas ejecutar un comando usa /ayuda para ver la lista.".format(mensaje_str)

		
# ----------------------------------------- Commands -----------------------------------------

# Bienvenida
def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=open("welcome.txt", "r").read(), parse_mode="Markdown")
	user_set.add(update.message.chat_id)
	user_list = str(user_set.count())
	bot.sendMessage(chat_id=update.message.chat_id, text="📡 Usuarios en línea: " + user_list)
	
# Manual
def manual(bot, update):
	bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
	manual_pdf = open("manual.pdf", "rb")
	time.sleep(1)
	bot.sendDocument(chat_id=update.message.chat_id, document=manual_pdf, filename="manual_SEKMUN_XI.pdf", caption="📄 Aquí tienes una versión optimizada para conexiones lentas del manual de SEKMUN XI")

# Status

def status(bot, update):
	timestamp_status = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
	reply = open("status.txt", "r", encoding="utf-8").read().format(moment=timestamp_status)
	bot.sendMessage(chat_id=update.message.chat_id, text=reply, parse_mode="Markdown")
	
# About

def about(bot, update):
	reply = open("about.txt", "r").read()
	bot.sendMessage(chat_id=update.message.chat_id, text=reply, parse_mode="Markdown")
	

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
status_handler = CommandHandler('status', status)
dispatcher.add_handler(status_handler)
about_handler = CommandHandler('about', about)
dispatcher.add_handler(about_handler)


# Message Handlers
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)
query_handler = MessageHandler(Filters.text, request_info)
dispatcher.add_handler(query_handler)


updater.start_polling()
updater.idle()