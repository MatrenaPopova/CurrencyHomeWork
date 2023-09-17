import telebot
from config import keys, TOKEN
from extansions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Привет, я - конвертер валют! \nЧтобы начать работу введите команду боту следующим образом: \n<имя валюты> <имя интересующей валюты> <количество валюты>, \nнапример: рубль доллар 1')

@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, 'Чтобы начать работу введите команду боту следующим образом: \n<имя валюты> <имя интересующей валюты> <количество валюты>, \nнапример: рубль доллар 1, \nЧтобы увидеть список всех доступных валют, введите команду\n/values')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):

    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)



bot.infinity_polling()