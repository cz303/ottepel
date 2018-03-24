import time
import datetime
import telebot
from telebot import types
import json
import calendar
import flask
import logging
from time import sleep
from slugify import slugify
from config import *
import urllib3
http = urllib3.PoolManager()

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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Ecommerce(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(255), unique=True)
    has_shop = db.Column(db.Boolean, default=False, nullable=False)
    market = db.Column(db.PickleType())
    location = db.Column(db.PickleType())
    domain = db.Column(db.String(255))

    def __init__(self, chat_id, has_shop=False, market=None, location=None, domain=None):
        self.chat_id = chat_id
        self.has_shop = has_shop
        self.market = market
        self.location = location
        self.domain = domain

    def __repr__(self):
        return '<Ecommerce %r>' % self.chat_id

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Integer)
    picture = db.Column(db.PickleType())
    market_id = db.Column(db.Integer)
    filled = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, name='', price=0, picture=None, market_id=0, filled=False):
        self.name = name
        self.price = price
        self.picture = picture
        self.market_id = market_id
        self.filled = filled

    def __repr__(self):
        return '<Item #%r>' % self.id


# create table
db.create_all()

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
@app.route('/', methods=['GET'])
def mainw():
    return '123'

@app.route('/merchant/<username>', methods=['GET'])
def index(username):
    one_item = Ecommerce.query.filter_by(domain=username).first()
    if not one_item:
        if username == '':
            # main domain, show all
            return '123'
        else:
            # redirect to main
            return flask.redirect("https://85.143.209.253:8443/", code=302)
    else:
        # this is merchant's subdomain
        return username


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
    chat_id = message.chat.id
    one_item = Ecommerce.query.filter_by(chat_id=chat_id).first()
    if not one_item.has_shop:
        markup.row(types.KeyboardButton('Создать магазин'))
    else:
        markup.row(types.KeyboardButton('Получить информацию о магазине'))
        markup.row(types.KeyboardButton('Добавить товар'))
        if Item.query.filter_by(market_id=chat_id).first():
            markup.row(types.KeyboardButton('Список товаров'))
        #markup.row(types.KeyboardButton('Вывести количество товаров'))
    bot.register_next_step_handler(message, process_choose)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    one_item = Ecommerce.query.filter_by(chat_id=chat_id).first()
    if not one_item:
        ecommerce_item = Ecommerce(chat_id)
        db.session.add(ecommerce_item)
        db.session.commit()
        # приветственное слово
        bot.send_message(message.chat.id, "Привет!", reply_markup=menu(message))
    else:
        bot.send_message(message.chat.id, "Выберите нужный пункт меню", reply_markup=menu(message))

def process_choose(message):
    chat_id = message.chat.id
    if message.text == 'Создать магазин':
        bot.send_message(chat_id, "Введите название магазина")
        bot.register_next_step_handler(message, new_market)
    elif message.text == 'Добавить товар':
        bot.send_message(chat_id, "Введитие название товара")
        bot.register_next_step_handler(message, new_items)
    elif message.text == 'Получить информацию о магазине':
        one_item = Ecommerce.query.filter_by(chat_id=chat_id).first()
        bot.send_message(chat_id, "Ваш магазин: '"+one_item.market+"' по адресу '"+one_item.location+"'")
        bot.send_message(chat_id, "Выберите нужный пункт меню", reply_markup=menu(message))
    #elif message.text == 'Вывести количество товаров': 
    #    all_items = Item.query.filter_by(market_id=chat_id).all()
    #    bot.send_message(chat_id, "У вас: " + str(len(all_items)) + " товаров")
    #    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)        
    #    for i in range(len(all_items)):
    #        keyboard.add(*[types.KeyboardButton('Название товара: ' + all_items[i].name + ' цена товара: ' + str(all_items[i].price))])
    #        #+ bot.send_photo(chat_id, all_items[i].picture))])
    #    bot.send_message(message.chat.id, 'ваш товар', reply_markup=keyboard)
    elif message.text == 'Список товаров':
        next_id = 0
        list_items = Item.query.filter_by(market_id=chat_id).all()
        markup = items_slider(chat_id, list_items, next_id)
        r = http.request('GET', str(list_items[next_id].picture))
        bot.send_photo(chat_id, r.data, reply_markup=markup)
    elif message.text.startswith('Редактировать товар #'):
        bot.send_message(chat_id, "Вы хотели отредактировать товар #" + message.text[21:], reply_markup=menu(message))
    else:
        bot.reply_to(message, "Команда не распознана")
        bot.send_message(chat_id, "Выберите нужный пункт меню", reply_markup=menu(message))

###### /HERE
def new_market(message):
    chat_id = message.chat.id
    one_item = Ecommerce.query.filter_by(chat_id=chat_id).first()
    one_item.market = message.text
    db.session.commit()
    bot.send_message(chat_id, "Вы ввели название " + one_item.market)
    bot.send_message(chat_id, "Введите желаемый поддомен:")
    bot.register_next_step_handler(message, new_slug)

def new_items(message):
    chat_id = message.chat.id
    new_item = Item(message.text, 0, None, chat_id)
    db.session.add(new_item)
    db.session.commit()
    one_item = Ecommerce.query.filter_by(chat_id=chat_id).first()
    bot.send_message(chat_id, "Введите цену товара")
    bot.register_next_step_handler(message, new_price)

def new_price(message):
    chat_id = message.chat.id
    one_item = Ecommerce.query.filter_by(chat_id=chat_id).first()
    try:
        a = int(message.text)
    except ValueError:
        bot.send_message(chat_id, "Введите верное значение")
        bot.register_next_step_handler(message, new_price)
    else:
        if a > 0:
            new_item = Item.query.filter_by(filled=False, market_id=chat_id).first()
            new_item.price = int(message.text)
            db.session.commit()
            bot.send_message(chat_id, "Цена " + str(new_item.price) + " добавлена")
            bot.send_message(chat_id, "Загрузите фото товара")
            bot.register_next_step_handler(message, new_picture)
            #bot.send_message(chat_id, "Выберите дальнейшее действие", reply_markup=menu(message))
        else:
            bot.send_message(chat_id, "Введите верное значение")
            bot.register_next_step_handler(message, new_price)

def new_slug(message):
    chat_id = message.chat.id
    domain_item = Ecommerce.query.filter_by(domain=message.text).first()
    if domain_item:
        bot.send_message(chat_id, "Такое доменное имя уже занято :( Введите другое:")
        bot.register_next_step_handler(message, new_slug)
    else:
        r = slugify(message.text)
        if r == message.text:
            one_item = Ecommerce.query.filter_by(chat_id=chat_id).first()
            one_item.domain = r
            db.session.commit()
            bot.send_message(chat_id, "ОК! Введите адрес вашего магазина:")
            bot.register_next_step_handler(message, new_location)
        else:
            bot.send_message(chat_id, "Используйте только латинские символы! Повторите ввод:")
            bot.register_next_step_handler(message, new_slug)

def new_picture(message):
    chat_id = message.chat.id
    new_item = Item.query.filter_by(filled=False, market_id=chat_id).first()
    if message.photo:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = 'https://api.telegram.org/file/bot' + API_TOKEN + '/' + file_info.file_path
        print(downloaded_file)
        new_item.picture = downloaded_file
        new_item.filled = True
        db.session.commit()
        bot.send_message(chat_id, "Выберите дальнейшее действие", reply_markup=menu(message))
    else:
        bot.send_message(chat_id, "Это была не картинка. Нужна Картинка!")
        bot.register_next_step_handler(message, new_picture)
    
def new_location(message):
    chat_id = message.chat.id
    one_item = Ecommerce.query.filter_by(chat_id=chat_id).first()
    one_item.location = message.text
    one_item.has_shop = True
    db.session.commit()
    bot.send_message(chat_id, "Ваш магазин добавлен. Магазин '"+one_item.market+ "' по адресу '"+ one_item.location+"'")
    bot.send_message(chat_id, "Выберите дальнейшее действие", reply_markup=menu(message))

def items_slider(chat_id, list_items, item_id):
    markup = types.InlineKeyboardMarkup()
    row=[]
    prev_id = item_id - 1
    next_id = item_id + 1

    if prev_id < 0:
        prev_id = len(list_items) - 1
    if next_id > len(list_items) - 1:
        next_id = 0

    row.append(types.InlineKeyboardButton("ID " + str(list_items[item_id].id) + " "+ list_items[item_id].name, callback_data="ignore"))

    markup.row(*row)
    row=[]
    if len(list_items) > 1:
        row.append(types.InlineKeyboardButton("<",callback_data="prev-item"+str(prev_id)))
        row.append(types.InlineKeyboardButton("В меню",callback_data="menu"))
        row.append(types.InlineKeyboardButton("Редактировать товар",callback_data="edit"+str(list_items[item_id].id)))
        row.append(types.InlineKeyboardButton(">",callback_data="next-item"+str(next_id)))
    else:
        row.append(types.InlineKeyboardButton("В меню",callback_data="menu"))
        row.append(types.InlineKeyboardButton("Редактировать товар",callback_data="edit"))
    markup.row(*row)
    return markup

@bot.callback_query_handler(func=lambda call: call.data[0:9] == 'next-item')
def next_item(call):
    chat_id = call.message.chat.id
    list_items = Item.query.filter_by(market_id=chat_id).all()
    item_num = int(call.data[9:])
    markup = items_slider(chat_id, list_items, item_num)
    bot.delete_message(call.from_user.id, call.message.message_id)
    r = http.request('GET', str(list_items[item_num].picture))
    bot.send_photo(call.from_user.id, r.data, reply_markup=markup)
    bot.answer_callback_query(call.id, text="")

@bot.callback_query_handler(func=lambda call: call.data[0:9] == 'prev-item')
def previous_item(call):
    chat_id = call.message.chat.id
    list_items = Item.query.filter_by(market_id=chat_id).all()
    item_num = int(call.data[9:])
    markup = items_slider(chat_id, list_items, item_num)
    bot.delete_message(call.from_user.id, call.message.message_id)
    r = http.request('GET', str(list_items[item_num].picture))
    bot.send_photo(call.from_user.id, r.data, reply_markup=markup)
    bot.answer_callback_query(call.id, text="")

@bot.callback_query_handler(func=lambda call: call.data == 'menu')
def to_menu(call):
    bot.send_message(call.message.chat.id, "Выберите дальнейшее действие", reply_markup=menu(call.message))


@bot.callback_query_handler(func=lambda call: call.data == 'edit')
def to_edit(call):
    bot.send_message(call.message.chat.id, "Редактируем #", reply_markup=menu(call.message))
    markup = types.InlineKeyboardMarkup()
    row=[]
    row.append(types.InlineKeyboardButton("Редактировать имя",callback_data="edit_name"))
    row.append(types.InlineKeyboardButton("Редактировать цену",callback_data="edit_price"))
    # row.append(types.InlineKeyboardButton("Редактировать товар",callback_data="edit"+str(list_items[item_id].id)))
    return markup

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
