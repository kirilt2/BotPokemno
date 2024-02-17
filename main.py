import time
import telebot
import requests
import sqlite3
from datetime import datetime

W = ''
#----------------------------------------------------------------|
API = 'https://api.exchangerate-api.com/v4/latest/'
BTC_API = 'https://api.coindesk.com/v1/bpi/currentprice.json'
Photo_API = 'https://picsum.photos/200/300'
#----------------------------------------------------------------|
bot = telebot.TeleBot(W)

#------Moeny--------------
Moeny = {
    'USD': 'Доллар США',
    'EUR': 'Евро',
    'GBP': 'Фунт стерлингов Великобритании',
    'JPY': 'Японская иена',
    'AUD': 'Австралийский доллар',
    'CAD': 'Канадский доллар',
    'CHF': 'Швейцарский франк',
    'CNY': 'Китайский юань',
    'SEK': 'Шведская крона',
    'NZD': 'Новозеландский доллар',
    'KRW': 'Южнокорейская вона',
    'SGD': 'Сингапурский доллар',
    'NOK': 'Норвежская крона',
    'MXN': 'Мексиканское песо',
    'INR': 'Индийская рупия',
    'RUB': 'Российский рубль',
    'ZAR': 'Южноафриканский рэнд',
    'BRL': 'Бразильский реал',
    'ILS': 'Израильский шекель',
    'BTC': 'Биткоин',
}
#-----------------------------------


def nameuser():
    conn = sqlite3.connect('MyBrainKiril/nameuser.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_interactions (
            id INTEGER PRIMARY KEY,
            username TEXT,
            user_id INTEGER,
            command TEXT,
            time TEXT
        )
    ''')
    conn.commit()
    conn.close()

nameuser()




@bot.message_handler(commands=['help', 'start', 'info'])
def bot1(message):
    list = "\n".join(f"{code}: {name}" for code, name in Moeny.items())
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message,f"Доступная валюта \n {list} \n Используйте команду /convert Сумма денег Название валюты И в какую валюту\n /convert 100 USD EUR")
    time.sleep(2)
    bot.send_message(message.chat.id,  f"это все команды которые вы можете использовать \n /convert конвертировать \n /subscribe Подписаться и получать уведомления \n /history Ваша недавняя история \n К примеру \n /convert 1 USD ILS \n /subscribe USD ILS \n /history")



@bot.message_handler(commands=['convert'])
def Cmoeny(message):
    list = "\n".join(f"{code}: {name}" for code, name in Moeny.items())
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(1)
        conn = sqlite3.connect('MyBrainKiril/nameuser.db')
        cursor = conn.cursor()
        command_parts = message.text.split()
        if len(command_parts) != 4:
            raise ValueError("Неправильный формат Пример использования: /convert Сумма денег Название валюты И в какую валюту \n /convert 100 USD EUR")
        MA = float(command_parts[1])
        CF = command_parts[2].upper()
        CT = command_parts[3].upper()

        exchange_rate = get_exchange_rate(CF, CT)
        if exchange_rate is None:
            if CF == 'BTC':
                raise ValueError(f"BTC К {CT} преобразование не поддерживается")
            else:
                raise ValueError(f"Cвалютная пара {CF}-{CT} не поддерживается\n {list}")

        converted_amount = MA * exchange_rate
        bot.send_message(message.chat.id,  f" {MA} {CF} Равно {converted_amount:.2f} {CT}")

        interaction_data = (message.from_user.username, message.from_user.id, message.text, str(datetime.now()))
        cursor.execute("INSERT INTO user_interactions (username, user_id, command, time) VALUES (?, ?, ?, ?)",
                       interaction_data)
        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        bot.reply_to(message, f" {str(e)}")
        print(f"{str(e)}")


@bot.message_handler(commands=['Ahistory'])
def adminA(message):
    if message.from_user.username != 'kiriilay':
        bot.reply_to(message, "у вас нет прав ._.")
        return
    try:
        conn = sqlite3.connect('MyBrainKiril/nameuser.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username, user_id, command, time FROM user_interactions")
        GF = cursor.fetchall()

        if GF:
            G = "История взаимодействия с пользователем \n"
            for interaction in GF:
                G += f" Username: {interaction[0]}, User ID: {interaction[1]}\n ------------------------------------------------------------------\n"
            bot.send_message(message.chat.id,  G)
        else:
            bot.reply_to(message, f"{str(Photo_API)}")

        cursor.close()
        conn.close()
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")






@bot.message_handler(commands=['history'])
def hi(message):
    try:
        conn = sqlite3.connect('MyBrainKiril/nameuser.db')
        cursor = conn.cursor()
        ID = message.from_user.id
        cursor.execute("SELECT command, time FROM user_interactions WHERE user_id = ? ORDER BY time DESC LIMIT 5", (ID,))
        H = cursor.fetchall()
        if H:
            response = "Ваша недавняя история\n"
            for command, time in H:
                response += f"- {command} at {time}\n"
            bot.send_message(message.chat.id,  response)
        else:
            bot.reply_to(message, "История конверсий не найдена")
        cursor.close()
        conn.close()
    except Exception as e:
        bot.send_message(message.chat.id, f"{str(e)}")
@bot.message_handler(commands=['Spam'])
def s(s):
    for g in range(10):
        g = requests.get(f'{Photo_API}')
        if g.status_code == 200:
            bot.send_photo(s.chat.id, g.content)


def get_exchange_rate(CF, CT):
    try:
        if CF == 'BTC':
            BTCR = requests.get(BTC_API)
            BTCD = BTCR.json()
            BTCR = BTCD['bpi']
            if CT in BTCR:
                return BTCR[CT]['rate_float']
            else:
                return None
        else:
            AR = requests.get(API + CF)
            data = AR.json()
            if 'rates' in data and CT in data['rates']:
                return data['rates'][CT]
            else:
                return None
    except Exception as e:
        bot.reply_to(f"Ошибка получения курса обмена {str(e)}")
        print(f"{str(e)}")
        return None



@bot.message_handler(commands=['Admin'])
def A(M):
    Username = "kiriilay"
    if M.from_user.username != Username:
        for f in range(5):
            bot.send_message(M.chat.id,  f"Ваше имя пользователя должно быть {Username}")
        return
    try:
        for w in range(5):

            S = requests.get(f'{Photo_API}')
            if S.status_code == 200:
                bot.send_photo(M.chat.id, S.content)
    except Exception as e:
        print(f"{str(e)}")



@bot.message_handler(commands=['subscribe'])
def Sub(SM):
    try:
        conn = sqlite3.connect('MyBrainKiril/subscriptions.db')
        cursor = conn.cursor()
        command_parts = SM.text.split()
        if len(command_parts) != 3:
            raise ValueError("Неправильный формат. Используйте: /subscribe ВАЛЮТА_ИЗ ВАЛЮТА_В")
        CF = command_parts[1].upper()
        CT = command_parts[2].upper()
        user_id = SM.from_user.id
        cursor.execute("INSERT INTO subscriptions (user_id, currency_from, currency_to) VALUES (?, ?, ?)", (user_id, CF, CT))
        conn.commit()
        bot.send_message(SM.chat.id,  f"Вы успешно подписались на оповещения курса {CF}-{CT}.")
        cursor.close()
        conn.close()
    except Exception as e:
        bot.reply_to(SM, f" {str(e)}")
        print(f" {str(e)}")

bot.polling()
