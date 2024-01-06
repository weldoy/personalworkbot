from telegram import Update, ParseMode, ReplyKeyboardRemove
from telegram.ext import CallbackContext, Filters, ConversationHandler, MessageHandler, CommandHandler

import logging
import requests
import json

from key import API_WEATHER

logger = logging.getLogger(__name__)

WAIT_CITY, WAIT_IP = range(2)


def ask_weather(update: Update, context: CallbackContext):
    logger.info(f'{update.effective_user.username} called the function - ask_weather')
    text = 'Here I can tell you about the weather in any city.\n'\
           'Write the town you want  - '

    context.bot.send_message(update.effective_chat.id, text, parse_mode=ParseMode.HTML,
                             reply_markup=ReplyKeyboardRemove())
    return WAIT_CITY


def get_weather(update: Update, context: CallbackContext):
    logger.info(f'{update.effective_user.username} called the function - get_weather')
    city = update.message.text.lower().strip()
    req = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_WEATHER}&units=metric')
    if req.status_code == 200:
        data = json.loads(req.text)
        text = f'Temp : {data["main"]["temp"]}\n'\
            f'This city in the country - {data["sys"]["country"]}'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                                 reply_markup=ReplyKeyboardRemove())
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='There is no such city.')
    return ConversationHandler.END


weather_handler = ConversationHandler(
    entry_points=[CommandHandler('weather', ask_weather)],
    states={
        WAIT_CITY: [MessageHandler(Filters.text, get_weather)],
    },
    fallbacks=[]
)


def ask_info_by_ip(update: Update, context: CallbackContext):
    logger.info(f'{update.effective_user.username} called the function - ask_info_by_ip')
    text = 'Please enter your target ip : '
    context.bot.send_message(update.effective_chat.id, text, reply_markup=ReplyKeyboardRemove())

    return WAIT_IP


def get_info_by_ip(update: Update, context: CallbackContext):
    logger.info(f'{update.effective_user.username} called the function - get_info_by_ip')
    try:
        ip = update.message.text
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()

        data = {
            '[IP]': response.get('query'),
            '[Int prov]': response.get('isp'),
            '[Org]': response.get('org'),
            '[Country]': response.get('country'),
            '[Region Name]': response.get('regionName'),
            '[City]': response.get('city'),
            '[ZIP]': response.get('zip'),
            '[Lat]': response.get('lat'),
            '[Lon]': response.get('lon'),
        }

        a = []
        for k, v in data.items():
            answer = f'{k} : {v}'
            a.append(f'{answer}\n')

        new_a = ''.join(a)
        context.bot.send_message(update.effective_chat.id, text=new_a,
                                 reply_markup=ReplyKeyboardRemove())

    except requests.exceptions.ConnectionError:
        context.bot.send_message(update.effective_chat.id, '[!] Please check your connection!',
                                 reply_markup=ReplyKeyboardRemove())
    except Exception:
        context.bot.send_message(update.effective_chat.id, '[!] Something goes wrong, try again!',
                                 reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


ip_handler = ConversationHandler(
    entry_points=[CommandHandler('ipinfo', ask_info_by_ip)],
    states={
        WAIT_IP: [MessageHandler(Filters.text, get_info_by_ip)],
    },
    fallbacks=[]
)
