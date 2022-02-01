import telebot

from config import TOKEN, keys
from extension import Converter, ConvertionException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'{message.chat.username}, write the currency You want to exchange in \
    "currency1 currency2 quantity" type \n To watch the list of currencies write "/values"')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'List of currencies:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):

    values = message.text.split(' ')
    values = list(map(str.lower, values))

    try:
        result = Converter.get_price(values)
    except ConvertionException as e:
        bot.reply_to(message, f"User's error \n{e}")
    except Exception as e:
        bot.reply_to(message, f"Can't handle command \n{e}")
    else:
        bot.send_message(message.chat.id, result)


bot.polling(none_stop=True)