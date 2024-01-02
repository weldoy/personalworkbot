from telegram import Update, ParseMode, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext import CallbackContext, Filters

import logging
import requests

from key import TOKEN
from fsm import weather_handler

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(name)s: %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def main():
    updater = Updater(token=TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', get_help))
    dp.add_handler(weather_handler)
    dp.add_handler(CommandHandler('btcvalue', get_btc_value))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    logger.info(updater.bot.getMe())
    updater.idle()


def start(update: Update, context: CallbackContext):
    logger.info(f'{update.effective_user.username} called the function - start')

    text = [
        f'Hi, <code>{update.effective_user.username}</code>!',
        '',
        f"I'm - <code>personalworkbot</code>.",
        f"I've a lot of things you can find if you type /help.",
        f'My owner on - <a href="github.com/weldoy">GitHub</a>.',
        '',
        f'Spend your time wisely.'
    ]
    text = '\n'.join(text)

    update.message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


def get_help(update: Update, context: CallbackContext):
    logger.info(f'{update.effective_user.username} called the function - help')
    text = [
        '<b>HELP</b>',
        '',
        f"There is i'll tell u about my arsenal :",
        '/weather - that will help you if you want to know the weather in cities.',
        '/btcvalue - it shows the latest BTC price.',
        '',
        'The rest is in development...'
    ]
    text = '\n'.join(text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML,
                             reply_markup=ReplyKeyboardRemove())


def get_btc_value(update: Update, context: CallbackContext):
    logger.info(f'{update.effective_user.username} called the function - get_btc_value')
    url = 'https://blockchain.info/ru/ticker'
    req = requests.get(url)
    req_json = req.json()
    answer = f'The latest price BTC - {float(req_json["USD"]["last"])}$'
    context.bot.send_message(update.effective_chat.id, answer, reply_markup=ReplyKeyboardRemove())


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Excuse me, i don't have that yet :(",
                             reply_markup=ReplyKeyboardRemove())


if __name__ == '__main__':
    main()
