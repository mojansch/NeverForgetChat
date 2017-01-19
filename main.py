# encoding: utf-8
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

updater = Updater(token='ZENSIERT')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.NOTSET)

updater.start_polling()


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Willkommen im Never Forget Chat!")
    klassenstufe = [[InlineKeyboardButton("7", callback_data='7')],
                    [InlineKeyboardButton("8", callback_data='8')],
                    [InlineKeyboardButton("9", callback_data='9')],
                    [InlineKeyboardButton("10", callback_data='10')],
                    [InlineKeyboardButton("11", callback_data='11')],
                    [InlineKeyboardButton("12", callback_data='12')]]
    klassenstufe_markup = InlineKeyboardMarkup(klassenstufe)
    update.message.reply_text('Wähle deine Klassenstufe:', reply_markup=klassenstufe_markup)


def button(bot, update):
    query = update.callback_query

    bot.editMessageText(text=u"Du bist in der Klassenstufe %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(CallbackQueryHandler(button))


def echo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)


echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)
