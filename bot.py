import time
import datetime
import telebot
from telebot import types
import json
import calendar
import flask
import hashlib
import logging
from time import sleep
from slugify import slugify
from config import *
import urllib3
http = urllib3.PoolManager()

WEBHOOK_SSL_CERT = '/etc/dehydrated/certs/dynamic-door.ru/fullchain.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = '/etc/dehydrated/certs/dynamic-door.ru/privkey.pem'  # Path to the ssl private key

#WEBHOOK_SSL_CERT = './server.crt'  # Path to the ssl certificate
#WEBHOOK_SSL_PRIV = './server.key'  # Path to the ssl private key
WEBHOOK_HOST = 'dynamic-door.ru'
# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

WEBHOOK_URL_BASE = "https://%s" % (WEBHOOK_HOST)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN, threaded=False)

app = flask.Flask(__name__, static_url_path='/static')


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
    api_bot = db.Column(db.String(255))
    pkey1 = db.Column(db.String(255))
    pkey2 = db.Column(db.String(255))
    merchant_id = db.Column(db.String(255))

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
    category_id = db.Column(db.Integer)
    filled = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, name='', price=0, picture=None, market_id=0, filled=False, category_id=0):
        self.name = name
        self.price = price
        self.picture = picture
        self.market_id = market_id
        self.category_id = category_id
        self.filled = filled

    def __repr__(self):
        return '<Item #%r>' % self.id

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    
    def __init__(self, name=''):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(255))
    market_id = db.Column(db.Integer)
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    item_id = db.Column(db.Integer)
    paid = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, chat_id='', market_id=0, item_id=0):
        self.chat_id = chat_id
        self.market_id = market_id
        self.item_id = item_id

    def __repr__(self):
        return '<Order for %r>' % self.chat_id


chat_dict ={}
chat_category={'Автомобили', 'Хобби', 'Чушь', 'и ещё', 'куча', 'всяких', 'категорий'}
# create table
db.create_all()


def get_pay_link(my_key, merchant_id, order_id, amount):
    data = {
        "request":{
            "order_id": order_id,
            "order_desc": "Оплата через eMarketBot",
            "currency":"RUB",
            "amount":amount,
            "merchant_id":merchant_id
        }
    }
    assert 'request' in data.keys()
    keys = sorted(data['request'].keys())
    values = [my_key]
    values += [data['request'][key] for key in keys]
    raw = '|'.join(values)
    data['request']['signature'] = hashlib.sha1(raw.encode('utf-8')).hexdigest()

    encoded_body = json.dumps(data)
    http = urllib3.PoolManager()
    r = http.request('POST', 'https://api.fondy.eu/api/checkout/redirect/',
        headers={'Content-Type': 'application/json'},
        body=encoded_body)

    return r.read()

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
    categories = Category.query.all()
    products = Item.query.all()
    return flask.render_template('index.html', categories=categories, products=products)

@app.route('/category/<catid>', methods=['GET'])
def category(catid):
    category = Category.query.filter_by(category_id=catid).first()
    products = Item.query.filter_by(category_id=category.id).all()
    return flask.render_template('category.html', category=category, products=products)

@app.route('/buy', methods=['POST'])
def buy():
    item_id = request.form.get('item')
    chat_id = request.form.get('chat_id')
    one_item = Item.query.filter_by(id=item_id).first()
    one_market = Ecommerce.query.filter_by(id=one_item.market_id).first()
    new_order = Orders(chat_id, one_item.market_id, one_item.id)
    db.session.add(new_order)
    db.session.commit()
    pay_link = get_pay_link(one_market.pkey1, one_market.merchant_id, new_order.id, one_item.price)
    return pay_link

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
        if Orders.query.filter_by(market_id=chat_id).first():
            markup.row(types.KeyboardButton('Список заказов'))
        markup.row(types.KeyboardButton('Настройки'))
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
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        new_cat = keyboard.add(*[types.KeyboardButton('Создать категорию')])
        for n in chat_category:
            keyboard.add(*[types.KeyboardButton('Категория: ' + n)])
        bot.send_message(message.chat.id, 'Выберите нужную категорию, если её нет, то создайте', reply_markup=keyboard)
        bot.register_next_step_handler(message, new_category)
    elif message.text == 'Получить информацию о магазине':
        one_item = Ecommerce.query.filter_by(chat_id=chat_id).first()
        bot.send_message(chat_id, "Ваш магазин: '"+one_item.market+"' по адресу '"+one_item.location+"'")
        bot.send_message(chat_id, "Выберите нужный пункт меню", reply_markup=menu(message))
    elif message.text == 'Список товаров':
        next_id = 0
        list_items = Item.query.filter_by(market_id=chat_id).all()
        markup = items_slider(chat_id, list_items, next_id)
        r = http.request('GET', str(list_items[next_id].picture))
        bot.send_photo(chat_id, r.data, reply_markup=markup)
    elif message.text == 'Список заказов':
        list_orders = Orders.query.filter_by(market_id=chat_id).all()
        string = ''
        for order in list_orders:
            item = Orders.query.filter_by(market_id=order.item_id).first()
            if order.paid:
                string += 'Оплаченный заказ #'+order.chat_id+' от @'+str(order.chat_id)+' '+str(order.datetime)+', товар: '+item.name+' за '+str(item.price)+'\n'
            else:
                string += 'НЕоплаченный заказ #'+order.chat_id+' от @'+str(order.chat_id)+' '+str(order.datetime)+', товар: '+item.name+' за '+str(item.price)+'\n'
        bot.send_message(chat_id, string, reply_markup=markup)
    elif message.text == 'Настройки':
        bot.send_message(chat_id, "Выберите нужный пункт настроек", reply_markup=menu_settings(message))
    else:
        bot.reply_to(message, "Команда не распознана")
        bot.send_message(chat_id, "Выберите нужный пункт меню", reply_markup=menu(message))

def menu_settings(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, selective=True)
    markup.row(types.KeyboardButton('api_bot - ключ из BotFather'))
    markup.row(types.KeyboardButton('Платежная система - pkey1'))
    markup.row(types.KeyboardButton('Платежная система - pkey2'))
    markup.row(types.KeyboardButton('Платежная система - Merchant id'))
    markup.row(types.KeyboardButton('Выйти'))
    bot.register_next_step_handler(message, process_settings)
    return markup


def process_settings(message):
    chat_id = message.chat.id
    if message.text == 'api_bot - ключ из BotFather':
        bot.send_message(chat_id, "Введите значение")
        bot.register_next_step_handler(message, change_key)
    elif message.text == 'Платежная система - pkey1':
        bot.send_message(chat_id, "Введите значение")
        bot.register_next_step_handler(message, change_pkey1)
    elif message.text == 'Платежная система - pkey2':
        bot.send_message(chat_id, "Введите значение")
        bot.register_next_step_handler(message, change_pkey2)
    elif message.text == 'Платежная система - Merchant id':
        bot.send_message(chat_id, "Введите значение")
        bot.register_next_step_handler(message, change_merchant_id)
    elif message.text == 'Выйти':
        bot.send_message(message.chat.id, "Выберите нужный пункт меню", reply_markup=menu(message))
    else:
        bot.reply_to(message, "Команда не распознана")
        bot.send_message(chat_id, "Выберите нужный пункт меню", reply_markup=menu_settings(message))

def change_key(message):
    chat_id = message.chat.id
    one_item = Ecommerce.query.filter_by(chat_id=chat_id).first()
    one_item.api_bot = message.text
    db.session.commit()
    
    bot.send_message(chat_id, "Сохранено! Выберите нужный пункт меню", reply_markup=menu_settings(message))

def change_pkey1(message):
    chat_id = message.chat.id
    one_item = Ecommerce.query.filter_by(chat_id=chat_id).first()
    one_item.pkey1 = message.text
    db.session.commit()
    bot.send_message(chat_id, "Сохранено! Выберите нужный пункт меню", reply_markup=menu_settings(message))

def change_pkey2(message):
    chat_id = message.chat.id
    one_item = Ecommerce.query.filter_by(chat_id=chat_id).first()
    one_item.pkey2 = message.text
    db.session.commit()
    bot.send_message(chat_id, "Сохранено! Выберите нужный пункт меню", reply_markup=menu_settings(message))

def change_merchant_id(message):
    chat_id = message.chat.id
    one_item = Ecommerce.query.filter_by(chat_id=chat_id).first()
    one_item.merchant_id = message.text
    db.session.commit()
    bot.send_message(chat_id, "Сохранено! Выберите нужный пункт меню", reply_markup=menu_settings(message))


def new_market(message):
    chat_id = message.chat.id
    one_item = Ecommerce.query.filter_by(chat_id=chat_id).first()
    one_item.market = message.text
    db.session.commit()
    bot.send_message(chat_id, "Вы ввели название " + one_item.market)
    bot.send_message(chat_id, "Введите желаемый поддомен:")
    bot.register_next_step_handler(message, new_slug)

def new_category(message):
    chat_id = message.chat.id
    one_item = Ecommerce.query.filter_by(chat_id=chat_id).first()
    msg = message.text
    if msg == 'Создать категорию':
        bot.send_message(chat_id, "Введите новую категорию")
        bot.register_next_step_handler(message, edit_cat)
    else:
        bot.register_next_step_handler(message, new_items)

def edit_cat:
    for n in chat_category:
        if message.text == n:
            bot.send_message(chat_id, "Данная категория существует, посмотрите внимательней")
            bot.register_next_step_handler(message, new_category)
        else:
            bot.send_message(chat_id, "Данная категория создана!")

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
        row.append(types.InlineKeyboardButton("Редактировать товар",callback_data="edit"+str(list_items[item_id].id)))
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


@bot.callback_query_handler(func=lambda call: call.data[0:4] == 'edit')
def to_edit(call):
    # get id of item
    chat_id = call.message.chat.id
    item_num = int(call.data[4:])
    bot.send_message(chat_id, "Выберите нужный пункт редактирования", reply_markup=edit_menu(call.message, item_num))
    
def edit_menu(message, item_num):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,selective=True)
    chat_id = message.chat.id
    chat_dict[chat_id] = item_num
    markup.row(types.KeyboardButton('Редактировать имя'))
    markup.row(types.KeyboardButton('Редактировать цену'))
    markup.row(types.KeyboardButton('Изменить картинку'))
    markup.row(types.KeyboardButton('В меню'))
    bot.register_next_step_handler(message, process_edit)
    return markup

def process_edit(message):
    chat_id = message.chat.id
    item_num = chat_dict[chat_id] # - тут у нас лежит id товара
    one_item = Ecommerce.query.filter_by(chat_id=chat_id).first()
    if message.text == 'Редактировать имя':
        bot.send_message(chat_id, "Введите новое название товара")
        bot.register_next_step_handler(message, change_item)
    elif message.text == 'Редактировать цену':
        bot.send_message(chat_id, "Введитие новую цену")
        bot.register_next_step_handler(message, change_price)
    elif message.text == 'Изменить картинку':
        bot.send_message(chat_id, "Загрузите новую картинку")
        bot.register_next_step_handler(message, change_picture)
    elif message.text == 'В меню':
         bot.send_message(chat_id, "Выберите дальнейшее действие", reply_markup=menu(message))
    else:
        bot.reply_to(message, "Команда не распознана")
        bot.send_message(chat_id, "Выберите нужный пункт редактирования", reply_markup=edit_menu(message, item_num))

def change_item(message):
    chat_id = message.chat.id
    item_num = chat_dict[chat_id]
    one_item = Item.query.filter_by(id=item_num).first()
    one_item.name = message.text
    db.session.commit()
    bot.send_message(chat_id, "Название изменено. Выберите нужный пункт редактирования", reply_markup=edit_menu(message, item_num)) 

def change_price(message):
    chat_id = message.chat.id
    item_num = chat_dict[chat_id]
    one_item = Item.query.filter_by(id=item_num).first()
    try:
        a = int(message.text)
    except ValueError:
        bot.send_message(chat_id, "Введите верное значение")
        bot.register_next_step_handler(message, change_price)
    else:
        if a > 0:
            one_item.price = a
            db.session.commit()
            bot.send_message(chat_id, "Цена изменена. Выберите нужный пункт редактирования", reply_markup=edit_menu(message, item_num))
        else:
            bot.send_message(chat_id, "Введите верное значение")
            bot.register_next_step_handler(message, change_price)

def change_picture(message):
    chat_id = message.chat.id
    item_num = chat_dict[chat_id]
    one_item = Item.query.filter_by(id=item_num).first()
    if message.photo:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = 'https://api.telegram.org/file/bot' + API_TOKEN + '/' + file_info.file_path
        print(downloaded_file)
        one_item.picture = downloaded_file
        one_item.filled = True
        db.session.commit()
        bot.send_message(chat_id, "Картинка изменена. Выберите нужный пункт редактирования", reply_markup=edit_menu(message, item_num))
    else:
        bot.send_message(chat_id, "Это была не картинка. Нужна Картинка!")
        bot.register_next_step_handler(message, new_picture)

# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()
sleep(1)
# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)#,certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Start flask server
app.run(host='127.0.0.1',
        port=WEBHOOK_PORT,
        #ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
        debug=True)