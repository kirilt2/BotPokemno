import telebot
import requests


TOKEN = ''
API = 'https://api.exchangerate-api.com/v4/latest/'
bot = telebot.TeleBot(TOKEN)


SUPPORTED_CURRENCIES = {
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
}


@bot.message_handler(commands=['help', 'start', 'info'])
def start(messges):
    list = "\n".join(f"{code}: {name}" for code, name in SUPPORTED_CURRENCIES.items())
    bot.reply_to(messges, f"Доступная валюта: {list} \n Используйте команду /convert Сумма денег  Название валюты И в какую валюту К примеру:\n /convert 100 USD EUR")


    @bot.message_handler(commands=['convert'])
    def Cmoeny(messges):
        try:
            command_parts = messges.text.split()
            if len(command_parts) != 4:
                raise ValueError("Неправильный формат наверно Попробуйте: /convert Сумма денег  Название валюты И в какую валюту К примеру: \n /convert 100 USD EUR")
            amout = float(command_parts[1])
            Cfrom = command_parts[2].upper()
            Cto = command_parts[3].upper()

            exchange_rate = get_exchange_rate(Cfrom, Cto)
            if exchange_rate is None:
                raise ValueError(f"Валюта не подержанная Посмотрите какие валюты есть: {list}")

            converted_amount = amout * exchange_rate
            bot.reply_to(messges, f" {amout} {Cfrom} Равно {converted_amount:.2f} {Cto}")

        except Exception as e:
            bot.reply_to(messges, f"Eroor {str(e)}")

    def get_exchange_rate(Cfrom, Cto):
        try:
            response = requests.get(Api + Cfrom)





bot.polling()
