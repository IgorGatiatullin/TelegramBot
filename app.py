import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CurrensyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def instructions(message: telebot.types.Message):
    text = 'Чтобы начать работу с ботом введите комманду в виде:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nПолучить список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)



@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    values = message.text.split(' ')

    if len(values) != 3:
        raise ConvertionException('Слишком много параметров.')

    quote, base, amount = values
    total_base = CurrensyConverter.get_price(quote, base, amount)

    m = float(round(total_base)*int(amount))
    text = f'Цена {amount} {quote} в {base} - {m}'
    bot.send_message(message.chat.id, text)

bot.polling()