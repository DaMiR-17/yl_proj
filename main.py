import telebot
from telebot import types
from ethermine import Ethermine
import requests  # Модуль для обработки URL
from bs4 import BeautifulSoup  # Модуль для работы с HTML
import time

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

ethermine = Ethermine()
stats = ethermine.network_stats()
check = False
name = ''
surname = ''
wall = ''
age = 0
adr = '825216ed8a6c4b25e9b6975c0843527b1398c273'
currency = Currency()
eth_usd = 'Курс к доллару: 1 ETH = ' + str(stats['usd']) + ' USD'
eth_btc = 'Курс к биткоину: 1 ETH = ' + str(stats['btc']) + ' BTC'
eth_rub = 'Курс к рублю: 1 ETH = ' + str(stats['usd'] * currency.check_currency())[:-2] + ' RUB'
usd_rub = 'Курс к рублю: 1 USD = ' + str(currency.check_currency())[:] + ' RUB'

bot = telebot.TeleBot("1761366351:AAHL95c2Se03pS_ZWzzmJObzG82pXmUWqWA")
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text == 'Привет':
        bot.send_message(message.from_user.id, 'Привет! ')
    elif message.text== "/start":
        bot.send_message(message.from_user.id, "Привет!")
        keyboard = types.InlineKeyboardMarkup()
        key_reg = types.InlineKeyboardButton(text='Зарегистрироваться', callback_data='reg')
        keyboard.add(key_reg)
        key_currency_ETH = types.InlineKeyboardButton(text='Узнать курс ETH', callback_data='currencyETH')
        keyboard.add(key_currency_ETH)
        key_currency_USD = types.InlineKeyboardButton(text='Узнать курс USD', callback_data='currencyUSD')
        keyboard.add(key_currency_USD)
        key_ferm = types.InlineKeyboardButton(text='Следить за майнинг-фермой', callback_data='ferm')
        keyboard.add(key_ferm)
        bot.send_message(message.from_user.id, text='Чем я могу тебе помочь?', reply_markup=keyboard)

    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Доступные команды:")
        bot.send_message(message.from_user.id, "/start - начало диалога")
        bot.send_message(message.from_user.id, "/eth_currency - курс ETH")
        bot.send_message(message.from_user.id, "/usd_currency - курс USD")
        bot.send_message(message.from_user.id, "/reg - регистрация")
        bot.send_message(message.from_user.id, "/add_ferm - добавление фермы")
        bot.send_message(message.from_user.id, "/stop - остановить отслеживание ферм")
    elif message.text == "/eth_currency":
        bot.send_message(message.from_user.id, eth_usd)
        bot.send_message(message.from_user.id, eth_btc)
        bot.send_message(message.from_user.id, eth_rub)
    elif message.text == "/usd_currency":
        bot.send_message(message.from_user.id, usd_rub)
    elif message.text == '/reg':
        bot.send_message(message.from_user.id, "Давай познакомимся! Как тебя зовут?")
        bot.register_next_step_handler(message, reg_name)
    elif message.text == '/stop':
        bot.send_message(message.from_user.id, "Хорошо, я больше не слежу за твоими фермами")
        keyboard = types.InlineKeyboardMarkup()
        key_reg = types.InlineKeyboardButton(text='Зарегистрироваться', callback_data='reg')
        keyboard.add(key_reg)
        key_currency_ETH = types.InlineKeyboardButton(text='Узнать курс ETH', callback_data='currencyETH')
        keyboard.add(key_currency_ETH)
        key_currency_USD = types.InlineKeyboardButton(text='Узнать курс USD', callback_data='currencyUSD')
        keyboard.add(key_currency_USD)
        key_ferm = types.InlineKeyboardButton(text='Следить за майнинг-фермой', callback_data='ferm')
        keyboard.add(key_ferm)
        bot.send_message(message.from_user.id, text='Чем я еще могу тебе помочь?', reply_markup=keyboard)
    elif message.text == '/add_ferm':
        bot.send_message(message.chat.id, "Введи свой кошелек: ")
        bot.register_next_step_handler(message, add_ferm)

def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Какая у вас фамилия?")
    bot.register_next_step_handler(message, reg_surname)

def reg_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "Сколько вам лет?")
    bot.register_next_step_handler(message, reg_age)

def reg_age(message):
    global age
    age = message.text
    while age == 0:
        try:
            age = int(message.text)
            age = message.text
        except Exception:
            bot.send_message(message.from_user.id, "Вводите цифрами!")

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Тебе ' + str(age) + ' лет? И тебя зовут: ' + name + ' ' + surname + '?'
    bot.send_message(message.from_user.id, text = question, reply_markup=keyboard)

def take_wall(message):
    bot.send_message(message.from_user.id, 'Введи свой кошелек: ')
    bot.register_next_step_handler(message, add_ferm)

def add_ferm(message):
    global wall
    wall = str(message.text)
    bot.send_message(message.from_user.id, 'Готово!')
    bot.send_message(message.from_user.id, 'Хотите узнать хэшрейт? (Да / Нет)')
    bot.register_next_step_handler(message, see_hash)

def see_hash(message):
    URL = f"https://api.ethermine.org/miner/{wall[2:]}/currentStats"
    r = requests.get(url=URL)
    data = r.json()
    hasherate = str(data['data']['reportedHashrate'])[:3] + '.' + str(data['data']['reportedHashrate'])[3:5]
    if message.text.lower() == 'да':
        bot.send_message(message.from_user.id, "Хэшрейт: " + str(hasherate) + ' Mh/s')
        keyboard = types.InlineKeyboardMarkup()
        key_reg = types.InlineKeyboardButton(text='Зарегистрироваться', callback_data='reg')
        keyboard.add(key_reg)
        key_currency_ETH = types.InlineKeyboardButton(text='Узнать курс ETH', callback_data='currencyETH')
        keyboard.add(key_currency_ETH)
        key_currency_USD = types.InlineKeyboardButton(text='Узнать курс USD', callback_data='currencyUSD')
        keyboard.add(key_currency_USD)
        key_ferm = types.InlineKeyboardButton(text='Следить за майнинг-фермой', callback_data='ferm')
        keyboard.add(key_ferm)
        bot.send_message(message.from_user.id, text='Что делаем дальше?', reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup()
        key_reg = types.InlineKeyboardButton(text='Зарегистрироваться', callback_data='reg')
        keyboard.add(key_reg)
        key_currency_ETH = types.InlineKeyboardButton(text='Узнать курс ETH', callback_data='currencyETH')
        keyboard.add(key_currency_ETH)
        key_currency_USD = types.InlineKeyboardButton(text='Узнать курс USD', callback_data='currencyUSD')
        keyboard.add(key_currency_USD)
        key_ferm = types.InlineKeyboardButton(text='Следить за майнинг-фермой', callback_data='ferm')
        keyboard.add(key_ferm)
        bot.send_message(message.from_user.id, text='Что делаем дальше?', reply_markup=keyboard)

def ferm_action(message):
    if message.text.lower() == 'да':
        keyboard = types.InlineKeyboardMarkup()
        key_add_ferm = types.InlineKeyboardButton(text='Добавить майнинг-ферму', callback_data='add_ferm')
        keyboard.add(key_add_ferm)
        key_hash_ferm = types.InlineKeyboardButton(text='Узнать хэшрейт', callback_data='hash_ferm')
        keyboard.add(key_hash_ferm)
        key_worker_ferm = types.InlineKeyboardButton(text='Показать фермы', callback_data='worker_ferm')
        keyboard.add(key_worker_ferm)
        key_check_ferm = types.InlineKeyboardButton(text='Отслеживать хэшрейт фермы', callback_data='check_ferm')
        keyboard.add(key_check_ferm)
        key_off_check_ferm = types.InlineKeyboardButton(text='Прекратить отслеживать хэшрейт фермы', callback_data='off_check_ferm')
        keyboard.add(key_off_check_ferm)
        bot.send_message(message.from_user.id, text='Что ты хочешь сделать?', reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup()
        key_reg = types.InlineKeyboardButton(text='Зарегистрироваться', callback_data='reg')
        keyboard.add(key_reg)
        key_currency_ETH = types.InlineKeyboardButton(text='Узнать курс ETH', callback_data='currencyETH')
        keyboard.add(key_currency_ETH)
        key_currency_USD = types.InlineKeyboardButton(text='Узнать курс USD', callback_data='currencyUSD')
        keyboard.add(key_currency_USD)
        key_ferm = types.InlineKeyboardButton(text='Следить за майнинг-фермой', callback_data='ferm')
        keyboard.add(key_ferm)
        bot.send_message(message.from_user.id, text='Что делаем дальше?', reply_markup=keyboard)

def worker_ferm(message):
    if message.text.lower() == 'да':
        bot.send_message(message.chat.id, "Вот ваши фермы: ")
        workers = ethermine.miner_workers(wall)
        all_hash = 0
        for i in range(len(workers)):
            if int(str(workers[i]['reportedHashrate'])[:3]) < 800:
                bot.send_message(message.from_user.id, str(i) + ' Worker ' + str(workers[i]['worker'])+ ' ' + str(workers[i]['reportedHashrate'])[:3] + '.' + str(workers[i]['reportedHashrate'])[3:5] + ' Mh/s')
                all_hash += float(str(workers[i]['reportedHashrate'])[:3] + '.' + str(workers[i]['reportedHashrate'])[3:5])
            else:
                bot.send_message(message.from_user.id, str(i) + ' Worker ' + str(workers[i]['worker'])+ ' ' + str(workers[i]['reportedHashrate'])[:2] + '.' + str(workers[i]['reportedHashrate'])[2:4] + ' Mh/s')
                all_hash += float(str(workers[i]['reportedHashrate'])[:2] + '.' + str(workers[i]['reportedHashrate'])[2:4])
        bot.send_message(message.from_user.id, 'All hashrate: ' + str(all_hash)[:6] + ' Mh/s')
        keyboard = types.InlineKeyboardMarkup()
        key_reg = types.InlineKeyboardButton(text='Зарегистрироваться', callback_data='reg')
        keyboard.add(key_reg)
        key_currency_ETH = types.InlineKeyboardButton(text='Узнать курс ETH', callback_data='currencyETH')
        keyboard.add(key_currency_ETH)
        key_currency_USD = types.InlineKeyboardButton(text='Узнать курс USD', callback_data='currencyUSD')
        keyboard.add(key_currency_USD)
        key_ferm = types.InlineKeyboardButton(text='Следить за майнинг-фермой', callback_data='ferm')
        keyboard.add(key_ferm)
        bot.send_message(message.from_user.id, text='Что делаем дальше?', reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup()
        key_reg = types.InlineKeyboardButton(text='Зарегистрироваться', callback_data='reg')
        keyboard.add(key_reg)
        key_currency_ETH = types.InlineKeyboardButton(text='Узнать курс ETH', callback_data='currencyETH')
        keyboard.add(key_currency_ETH)
        key_currency_USD = types.InlineKeyboardButton(text='Узнать курс USD', callback_data='currencyUSD')
        keyboard.add(key_currency_USD)
        key_ferm = types.InlineKeyboardButton(text='Следить за майнинг-фермой', callback_data='ferm')
        keyboard.add(key_ferm)
        bot.send_message(message.from_user.id, text=name.title() + ', что делаем дальше?', reply_markup=keyboard)

def check_ferm(message):
    if message.text.lower() == 'да':
        check = True
        bot.send_message(message.chat.id, "Введите необходимый хэшрейт, и если он упадет ниже указанного, то вы будете уведомлены! ")
        bot.register_next_step_handler(message, checking_ferm)
    else:
        keyboard = types.InlineKeyboardMarkup()
        key_reg = types.InlineKeyboardButton(text='Зарегистрироваться', callback_data='reg')
        keyboard.add(key_reg)
        key_currency_ETH = types.InlineKeyboardButton(text='Узнать курс ETH', callback_data='currencyETH')
        keyboard.add(key_currency_ETH)
        key_currency_USD = types.InlineKeyboardButton(text='Узнать курс USD', callback_data='currencyUSD')
        keyboard.add(key_currency_USD)
        key_ferm = types.InlineKeyboardButton(text='Следить за майнинг-фермой', callback_data='ferm')
        keyboard.add(key_ferm)
        bot.send_message(message.from_user.id, text=name.title() + ', что делаем дальше?', reply_markup=keyboard)
def checking_ferm(message):
    h = int(message.text)
    workers = ethermine.miner_workers(wall)
    while check:
        all_hash = 0
        for i in range(len(workers)):
            if int(str(workers[i]['reportedHashrate'])[:3]) < 800:
                bot.send_message(message.from_user.id, str(i) + 'Worker ' + workers[i]['worker'], str(workers[i]['reportedHashrate'])[:3] + '.' + str(workers[i]['reportedHashrate'])[3:5] + ' Mh/s')
                all_hash += float(str(workers[i]['reportedHashrate'])[:3] + '.' + str(workers[i]['reportedHashrate'])[3:5])
            else:
                bot.send_message(message.from_user.id, str(i) + 'Worker ' + workers[i]['worker'], str(workers[i]['reportedHashrate'])[:2] + '.' + str(workers[i]['reportedHashrate'])[2:4] + ' Mh/s')
                all_hash += float(str(workers[i]['reportedHashrate'])[:2] + '.' + str(workers[i]['reportedHashrate'])[2:4])
        if all_hash < h:
            bot.send_message(message.from_user.id, str(all_hash) + ' Mh/s')
        time.sleep(600)
    keyboard = types.InlineKeyboardMarkup()
    key_reg = types.InlineKeyboardButton(text='Зарегистрироваться', callback_data='reg')
    keyboard.add(key_reg)
    key_currency_ETH = types.InlineKeyboardButton(text='Узнать курс ETH', callback_data='currencyETH')
    keyboard.add(key_currency_ETH)
    key_currency_USD = types.InlineKeyboardButton(text='Узнать курс USD', callback_data='currencyUSD')
    keyboard.add(key_currency_USD)
    key_ferm = types.InlineKeyboardButton(text='Следить за майнинг-фермой', callback_data='ferm')
    keyboard.add(key_ferm)
    bot.send_message(message.from_user.id, text='Что делаем дальше?', reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "currencyETH":  # call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.from_user.id, eth_usd)
        bot.send_message(call.from_user.id, eth_btc)
        bot.send_message(call.from_user.id, eth_rub)
    elif call.data == "currencyUSD":
        bot.send_message(call.from_user.id, usd_rub)
    elif call.data == "ferm":
        bot.send_message(call.from_user.id, name.title() + ', у вас есть своя майнинг-ферма? (Да / Нет)')
        bot.register_next_step_handler(call.message, ferm_action)
    elif call.data == "hash_ferm":
        global wall
        URL = f"https://api.ethermine.org/miner/{wall[2:]}/currentStats"
        r = requests.get(url=URL)
        data = r.json()
        hasherate = str(data['data']['reportedHashrate'])[:3] + '.' + str(data['data']['reportedHashrate'])[3:5]
        bot.send_message(call.message.chat.id, "Хэшрейт: " + str(hasherate)   + ' Mh/s')

    elif call.data == "add_ferm":
        bot.send_message(call.message.chat.id, name.title() + ", введи свой кошелек: ")
        bot.register_next_step_handler(call.message, add_ferm)
    elif call.data == "worker_ferm":
        bot.send_message(call.message.chat.id, name.title() + ", вы указали свой кошелек? (Да / Нет)")
        bot.register_next_step_handler(call.message, worker_ferm)
    elif call.data == "check_ferm":
        bot.send_message(call.message.chat.id, name.title() + ", вы хотите отслеживать свои фермы? (Да / Нет)")
        bot.register_next_step_handler(call.message, check_ferm)
    elif call.data == "off_check_ferm":
        bot.send_message(call.message.chat.id, name.title() + ", я прекратил отслеживать хэшрейт фермы")
        bot.send_message(call.message.chat.id, "Можешь написать /start , что бы увидеть список команд)")
    elif call.data == "reg":
        bot.send_message(call.message.chat.id, "Давай познакомимся! Как тебя зовут?")
        bot.register_next_step_handler(call.message, reg_name)
    elif call.data == "yes":
        bot.send_message(call.message.chat.id, "Приятно познакомиться, " + name.title() + "!")
        bot.send_message(call.message.chat.id, "Можешь написать /help , что бы увидеть список доступных команд)")
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Попробуем еще раз!")
        bot.send_message(call.message.chat.id, "Давай познакомимся! Как тебя зовут?")
        bot.register_next_step_handler(call.message, reg_name)

bot.polling()