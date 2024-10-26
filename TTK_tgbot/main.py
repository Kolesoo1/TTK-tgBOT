from telebot import types
import re
import telebot
from User import User

bot = telebot.TeleBot('7897016753:AAF8OAJ8jXWRpDyCOrHM344rW8zUEXTX-_c')

@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_log_in = types.InlineKeyboardButton(text='1. Войти как клиент ТТК', callback_data='log_in')  # кнопка «Да»
    keyboard.add(key_log_in)  # добавляем кнопку в клавиатуру
    key_set_up = types.InlineKeyboardButton(text='2. Заключить новый договор', callback_data='set_up')
    keyboard.add(key_set_up)
    bot.send_message(message.chat.id, 'Здравствуйте! Рады видеть Вас на платформе Акционерного общества «Компания ТрансТелеКом». '
                                      'Выберете действие: для этого вам нужно нажать одну из кнопок', reply_markup=keyboard)





@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "log_in": #call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.from_user.id, 'Введите номер договора')
        bot.register_next_step_handler_by_chat_id(call.from_user.id, get_reg_number)

    elif call.data == "set_up":
        bot.send_message(call.message.chat.id, 'Чтобы начать работу, нам нужно задавать два вопроса'
                                               'Сначала, пожалуйста, сообщите Ваш контактный номер телефона в формате: 8xxxxxxxxxxx.')
        bot.register_next_step_handler_by_chat_id(call.from_user.id, get_number)

def get_reg_number(message):
    global reg_number
    if bool(re.search(r'\d{9}', message.text)):
        reg_number = message.text
    else:
        bot.send_message(message.from_user.id, 'Номер договора это комбинация из 9 цифр')
        bot.register_next_step_handler_by_chat_id(message.from_user.id, get_reg_number)
        return

def get_number(message):
    global phone_number
    if bool(re.search(r'8\d{10}', message.text)):
        phone_number = message.text
    else:
        bot.send_message(message.from_user.id, 'Номер телефона набран неправильно. Повторите, пожалуйста, ввод')
        bot.register_next_step_handler_by_chat_id(message.from_user.id, get_number)
        return 

    bot.send_message(message.from_user.id, 'Отлично, спасибо!\nУточните, пожалуйста, свой полный адрес.')
    bot.register_next_step_handler_by_chat_id(message.from_user.id, get_address)


def get_address(message):
    global address
    address = message.text
    user = User(phone_number, address)
    bot.send_message(message.from_user.id, 'Благодарим за ответы! Вам присвоен персональный номер договора: ' + user.get_reg_number())
    #bot.register_next_step_handler_by_chat_id(message.from_user.id, get_address(User))




def generate_reg_number(message):
    return
bot.polling(none_stop=True)