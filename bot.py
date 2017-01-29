#! python3
# -*- coding: utf-8 -*

"""
search.py - Módulo de consulta de información para SEKMUN Bot

SEKMUN Bot desarrollado por Marcos Gómez (http://margobra8.ml/)
Distribuido bajo la licencia MIT (ver LICENSE.md)
"""

# Librerías base
import re
import time
from datetime import datetime

# Librerías base de python-telegram-bot
from telegram.ext import Updater, CommandHandler

# Importación de MessageHandler
from telegram.ext import MessageHandler, Filters
from telegram.chataction import ChatAction

# Importar el módulo de consulta
# from search import info_query // TODO: No Funciona

# Instanciar el bot y los thread Dispatcher y Updater
from config import TOKEN
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# Logging
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Lista de Usuarios
user_set = set()


# Términos de búsqueda e información en Regex
paths = {
	r"(?i)moci[oó]?n(es)? de (procedimiento)s?": "mociones/mocion_procedimiento.txt",
	r"(?i)moci[oó]?n(es)? de [óo]?rden(es)?": "mociones/mocion_orden.txt",
	r"(?i)moci[oó]?n(es)? de duda(s)?": "mociones/mocion_duda.txt",
	r"(?i)moci[oó]?n(es)? de (privilegio)s?": "mociones/mocion_privilegio.txt",
	r"(?i)moci[oó]?n(es)?": "mociones/mociones.txt",
	r"(?i)caucus simples?": "caucus/simple.txt",
	r"(?i)caucus moderados?": "caucus/moderado.txt",
	r"(?i)caucus": "caucus/index.txt",
	r"(?i)defender.+?anteproyectos?": "debate_particular/index.txt",
	r"(?i)debates?": "debate_particular/index.txt",
	r"(?i)anteproyectos?": "anteproyecto/index.txt",
}

# Errores de búsqueda
error_notfound = "❌ _*ERROR*_\n\nNo se han encontrado resultados de búsqueda para\n<`{query}`> 😕\n\nSi necesitas ejecutar un comando usa /ayuda para ver la lista."

# Main method
def info_query(msg):
	for regex, path in paths.items():	
		logging.info("SCAN " + regex)
		if re.search(regex, msg):
			time.sleep(0.1)
			logging.info("FOUND " + regex)
			return open(path).read()
					
		else:
			NotFound = True
	if NotFound:
		logging.info("NOT FOUND " + msg)
		return error_notfound.format(query=msg)
		
# ----------------------------------------- Comandos -----------------------------------------

# Bienvenida
def start(bot, update):
	# Enviar mensaje de bienvenida/ayuda
	bot.sendMessage(chat_id=update.message.chat_id, text=open("welcome.txt", "r").read(), parse_mode="Markdown")
	# Añadir al set de todos los usuarios (para broadcasts y eso)
	user_set.add(update.message.chat_id)
	#Log en consola
	logging.info("CONNECTED " + str(update.message.chat_id))
	# Añadir los nombres reales de las personas para estadística a un fichero externo
	to_append = str(update.message.chat_id) + " -- " + update.message.from_user.name + "\n"
	if update.message.from_user.name not in open('usernamelist.txt').read():		
		with open("usernamelist.txt", "a") as userlog:
			userlog.write(to_append)
	# Responder con la cuenta de usuarios activos
	response = "📡 {} usuarios en línea".format(str(len(user_set)))
	bot.sendMessage(chat_id=update.message.chat_id, text=response, parse_mode="Markdown")
	
def ayuda(bot, update):
	# Enviar mensaje de bienvenida/ayuda
	bot.sendMessage(chat_id=update.message.chat_id, text=open("welcome.txt", "r").read(), parse_mode="Markdown")
	
# Manual
def manual(bot, update):
	bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
	manual_pdf = open("manual.pdf", "rb")
	time.sleep(1)
	bot.sendDocument(chat_id=update.message.chat_id, document=manual_pdf, filename="manual_SEKMUN_XI.pdf", caption="📄 Aquí tienes una versión optimizada para conexiones lentas del manual de SEKMUN XI")

# Status
def status(bot, update):
	timestamp_status = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
	response = open("status.txt", "r", encoding="utf-8").read().format(moment=timestamp_status)
	bot.sendMessage(chat_id=update.message.chat_id, text=reply, parse_mode="Markdown")
	
# About
def about(bot, update):
	reply = open("about.txt", "r").read()
	bot.sendMessage(chat_id=update.message.chat_id, text=reply, parse_mode="Markdown")
	

# Comando Desconocido
def unknown(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Lo siento, no reconozco ese comando 😕")

# --------------------------------------------------------------------------------------------
	
# Evento de texto normal
def text_parser(bot, update):
	message = update.message.text
	logging.info("QUERY RX " + str(update.message.chat_id) + ": " +  message)
	bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
	response = info_query(message)
	bot.sendMessage(chat_id=update.message.chat_id, text=response, parse_mode="Markdown")
	logging.info("TX")
	
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
query_handler = MessageHandler(Filters.text, text_parser)
dispatcher.add_handler(query_handler)

# Iniciar bot
updater.start_polling()
updater.idle()