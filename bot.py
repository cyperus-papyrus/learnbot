from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from settings import PROXY, API_KEY
import ephem, datetime

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(bot, update):
    text = 'Вызван /start'
    logging.info(text)
    update.message.reply_text(text)


def about_planet(bot, update):
    message = update.message.text
    logging.info(message)
    planet_name = message.split(' ')[1]
    try:
        planet_info = getattr(ephem, planet_name)(datetime.datetime.today())
        constellation = ephem.constellation(planet_info)
        update.message.reply_text(constellation[1])
    except AttributeError:
        update.message.reply_text('Planet "{}" doesn\'t exist! Try any of those: Mercury, '
                                  'Venus, Mars, Jupiter, Saturn, Uranus, '
                                  'Neptune'.format(planet_name))


def talk_to_me(bot, update):
    user_text = "Привет, {}! Ты написал: {} ".format(update.message.chat.first_name, update.message.text)
    logging.info("User: %s, Chat ID: %s, Message: %s", update.message.chat.username,
                 update.message.chat.id,
                 update.message.text)
    update.message.reply_text(user_text)


def main():
    mybot = Updater(API_KEY, request_kwargs=PROXY)
    logging.info('Бот запускается')
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", about_planet))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
