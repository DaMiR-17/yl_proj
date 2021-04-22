from ethermine import Ethermine
# from telegram.ext import Updater, MessageHandler, Filters
# from telegram.ext import CallbackContext, CommandHandler
# from telegram import ReplyKeyboardMarkup
import telebot
from telebot import types
import requests  # Модуль для обработки URL
from bs4 import BeautifulSoup  # Модуль для работы с HTML
import time  # Модуль для остановки программы
bot = telebot.TeleBot('1761366351:AAHL95c2Se03pS_ZWzzmJObzG82pXmUWqWA')

ethermine = Ethermine()
stats = ethermine.pool_stats()
stats = ethermine.network_stats()
history = ethermine.blocks_history()
workers = ethermine.miner_workers("0x825216ed8a6c4b25e9b6975c0843527b1398c273")
history = ethermine.miner_history("0x825216ed8a6c4b25e9b6975c0843527b1398c273")
payouts = ethermine.miner_payouts("0x825216ed8a6c4b25e9b6975c0843527b1398c273")

# print('Время добычи 1 блока:', stats['blockTime'], 'секунд'


class Currency:
    # Ссылка на нужную страницу
    DOLLAR_RUB = 'https://www.google.com/search?sxsrf=ALeKk01NWm6viYijAo3HXYOEQUyDEDtFEw%3A1584716087546&source=hp&ei=N9l0XtDXHs716QTcuaXoAg&q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+&gs_l=psy-ab.3.0.35i39i70i258j0i131l4j0j0i131l4.3044.4178..5294...1.0..0.83.544.7......0....1..gws-wiz.......35i39.5QL6Ev1Kfk4'
    # Заголовки для передачи вместе с URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    current_converted_price = 0

    def __init__(self):
        # Установка курса валюты при создании объекта
        self.current_converted_price = float(self.get_currency_price().replace(",", "."))

    # Метод для получения курса валюты
    def get_currency_price(self):
        # Парсим всю страницу
        full_page = requests.get(self.DOLLAR_RUB, headers=self.headers)

        # Разбираем через BeautifulSoup
        soup = BeautifulSoup(full_page.content, 'html.parser')

        # Получаем нужное для нас значение и возвращаем его
        convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        return convert[0].text

    def check_currency(self):
        currency = float(self.get_currency_price().replace(",", "."))
        return currency


name = ''
surname = ''
age = 0
adr = '825216ed8a6c4b25e9b6975c0843527b1398c273'
currency = Currency()
eth_usd = 'Курс к доллару: 1 ETH = ' + str(stats['usd']) + ' USD'
eth_btc = 'Курс к биткоину: 1 ETH = ' + str(stats['btc']) + ' BTC'
eth_rub = 'Курс к рублю: 1 ETH = ' + str(stats['usd'] * currency.check_currency())[:-2] + ' RUB'
URL = f"https://api.ethermine.org/miner/{adr}/currentStats"
bot = telebot.TeleBot("1761366351:AAHL95c2Se03pS_ZWzzmJObzG82pXmUWqWA")
r = requests.get(url = URL)
data = r.json()
hasherate = int(str(data['data']['reportedHashrate'])[:3])

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, str(hasherate) + ' Mh/s')
    if hasherate < 780:
        bot.send_message(message.from_user.id, str(hasherate) + ' Mh/s')
    elif message.text.lower() == "/start":
        bot.send_message(message.from_user.id, "Привет! Хочешь узнать курс ETH?")
        keyboard = types.InlineKeyboardMarkup()
        key_currency = types.InlineKeyboardButton(text='Курс ETH', callback_data='currency')
        keyboard.add(key_currency)
        key_ferm = types.InlineKeyboardButton(text='Добавить ферму', callback_data='ferm')
        keyboard.add(key_ferm)
        bot.send_message(message.from_user.id, text='Что ты хочешь сделать?', reply_markup=keyboard)

    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Доступные команды:")
        bot.send_message(message.from_user.id, "/eth_currency - курс")
        bot.send_message(message.from_user.id, "/reg - регистрация")
        bot.send_message(message.from_user.id, "/")
        bot.send_message(message.from_user.id, "/")
    elif message.text == "/eth_currency":
        bot.send_message(message.from_user.id, eth_usd)
        bot.send_message(message.from_user.id, eth_btc)
        bot.send_message(message.from_user.id, eth_rub)
    elif message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name

    else:
        bot.send_message(message.from_user.id, 'Напиши /help')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "currency":  # call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.from_user.id, eth_usd)
        bot.send_message(call.from_user.id, eth_btc)
        bot.send_message(call.from_user.id, eth_rub)
    elif call.data == "ferm":
        bot.send_message(call.from_user.id, 'Введите ваш ETH кошелек')
        name = message.text

def get_name(message):  # получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    while age == 0:  # проверяем что возраст изменился
        try:
             age = int(message.text)  # проверяем, что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        # ....# код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id, 'Запомню : )')
    elif call.data == "no":
        bot.send_message(call.from_user.id, 'Напиши /reg')


bot.polling(none_stop=True, interval=0)





