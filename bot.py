import time
import datetime
import telebot
from telebot import types
import json
import calendar

API_TOKEN = 'here code'

bot = telebot.TeleBot(API_TOKEN)

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

bot.polling()
