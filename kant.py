from telegram.ext import Updater
import logging
import sqlite3

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

connection = sqlite3.connect('kant.db', check_same_thread=False)
cursor = connection.cursor()
cursor.execute('SELECT COUNT(*) FROM quotes')
amount = cursor.fetchone()[0]

with open('token', 'r') as f:
    token = f.read()


def help(bot, update):
    global amount
    text = "Бот-филасаф. В базе %s цитат.\n/get_quote - получить цитату." % amount
    bot.sendMessage(update.message.chat_id, text=text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def get_quote(bot, update):
    global cursor
    query = 'SELECT `text` FROM quotes ORDER BY RANDOM() LIMIT 1'
    cursor.execute(query)
    message = cursor.fetchone()[0]
    bot.sendMessage(update.message.chat_id, text=message)


def main():
    global token
    updater = Updater(token)
    dp = updater.dispatcher
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("get_quote", get_quote)
    dp.addErrorHandler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
