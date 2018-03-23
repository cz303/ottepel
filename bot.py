import time
import datetime
import telebot
from telebot import types
import json
import calendar
import flask
import logging
from time import sleep

API_TOKEN = '589097589:AAGaYpjDEBhWwL4Ukfn_jXnBMA69Tygrwp4'

WEBHOOK_HOST = 'dynamic-door.ru'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '85.143.209.253'
#'0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = '/etc/dehydrated/certs/dynamic-door.ru/fullchain.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = '/etc/dehydrated/certs/dynamic-door.ru/privkey.pem'  # Path to the ssl private key

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

app = flask.Flask(__name__)


# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

###### HERE

def menu(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,selective=True)
    markup.row(types.KeyboardButton('Вопрос-ответ'))
    bot.register_next_step_handler(message, process_choose)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, "+message.chat.first_name + ' ' +message.chat.last_name + '!', reply_markup=menu(message))


def process_choose(message):
    chat_id = message.chat.id
    if message.text == 'Вопрос-ответ':
        bot.send_message(chat_id, "123")
        bot.register_next_step_handler(message, process_choose)
    else:
        bot.reply_to(message, "Команда не распознана")
        bot.register_next_step_handler(message, process_choose)

###### /HERE



# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()
sleep(1)
# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Start flask server
app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
        debug=True)

