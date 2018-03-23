import time
import datetime
import telebot
from telebot import types
import json
import calendar
import flask
import logging
from time import sleep

from config import *

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = '/etc/dehydrated/certs/dynamic-door.ru/privkey.pem'  # Path to the ssl private key

WEBHOOK_SSL_CERT = './server.crt'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './server.key'  # Path to the ssl private key

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

bot = telebot.TeleBot(API_TOKEN, threaded=False)

app = flask.Flask(__name__)


###### DB
from flask_sqlalchemy import SQLAlchemy


app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG
db = SQLAlchemy(app)


class Ecommerce(db.Model):
    chat_id = db.Column(db.String(255), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

# create table
# db.create_all()

## СМОТРИ ТУТ!
# --Добавляем нового чувака в базу, заполняем поля:
# ecommerce_item = Ecommerce('admin', 'admin@example.com')
# --Добавляем в БД:
# db.session.add(ecommerce_item)
# db.session.commit()
# 
# -- Чтобы получить:
# items = Ecommerce.query.all() # все
# -- Получить конкретные:
# items = Ecommerce.query.filter_by(chat_id='123321').all()
# -- Получить одну запись:
# one_item = Ecommerce.query.filter_by(chat_id='123321').first()


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


class Chat:
    def __init__(self):
        self.has_shop = None
        self.market = None
        self.items = []
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

chat_dict = {}
users = []

def menu(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,selective=True)
    chat_id = message.chat.id
    if not chat_dict[chat_id].has_shop:
        markup.row(types.KeyboardButton('Создать магазин'))
    else:
        markup.row(types.KeyboardButton('Добавить товар'))
        markup.row(types.KeyboardButton('Вывести товары'))
    bot.register_next_step_handler(message, process_choose)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    chat = Chat()
    if chat_id not in chat_dict:
        chat_dict[chat_id] = chat
        bot.send_message(message.chat.id, "Привет, "+message.chat.first_name + ' ' +message.chat.last_name + '!', reply_markup=menu(message))
    else:
        bot.send_message(message.chat.id, "Сперва введите /start")

def process_choose(message):
    chat_id = message.chat.id
    if message.text == 'Вопрос-ответ':
        bot.send_message(chat_id, "123")
        bot.register_next_step_handler(message, process_choose)
    elif message.text == 'Создать магазин':
        bot.send_message(chat_id, "Введите название магазина")
        bot.register_next_step_handler(message, new_market)
    elif message.test == 'Добавить товар':
        bot.send_message(chat_id, "Введитие название товара")
        bot.register_next_step_handler(message, new_items)
    else:
        bot.reply_to(message, "Команда не распознана")
        bot.register_next_step_handler(message, process_choose)

###### /HERE

def new_market(message):
    chat_id = message.chat.id
    chat_dict[chat_id].market = message.text
    bot.send_message(chat_id, "Вы ввели название " + chat_dict[chat_id].market)
    bot.register_next_step_handler(message, process_choose)

def new_items(message):
    chat_id = message.chat.id
    chat_dict[chat_id].items.append({'name': message.text})
    bot.send_message(chat_id, "Товар " + chat_dict[chat_id].items + " добавлен")
    bot.send_message(chat_id, "Введите цену товара")
    bot.register_next_step_handler(message, new_price)

def new_price(message):
    if message.text.isdigit() == True and message.test > 0:
        chat_id = message.chat.id
        chat_dict[chat_id].items.append({'price':message.text})
        bot.send_message(chat_id, "Цена " + chat_dict[chat_id].items + " добавлена")
        bot.send_message(chat_id, chat_dict[chat_id].items)
        bot.register_next_step_handler(message, process_choose)
    else:
        bot.send_message(chat_id, "Введите верное значение")
        bot.register_next_step_handler(message, new_price)


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

