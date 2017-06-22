#!/usr/bin/env python
# -*- coding: utf-8 -*-


from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

default = 'default'
#fixme GLOBALE VARIABLE fragfach ERSETZEN
fragfach = ''
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.NOTSET)

logger = logging.getLogger(__name__)

KLASSE, HAUPTMENUE, FRAGE, FRAGEN, FRAGEN2, HAUPTMENUE, BEANTWORTEN = range(7)


def start(bot, update):
    user = update.message.from_user
    if user.username == '':
        update.message.reply_text(
            'Um den Never Forget Chat zu nutzen, musst du in den Telegram-Einstellungen jetzt einen Benutzernamen festlegen. \n\nBei Fragen wende dich an @sn0w_man')
        logger.info(user.first_name,user.last_name,' hat keinen Benutzernamen')
    klasse_keyboard = [['7','8'],
                      ['9','10'],
                      ['11','12']]

    update.message.reply_text(
        'Willkommen zur Never Forget Chat Demo!\n'
        'Wähle deine Klassenstufe: ',
        reply_markup=ReplyKeyboardMarkup(klasse_keyboard, one_time_keyboard=True))

    return KLASSE


def klasse(bot, update):
    user = update.message.from_user
    logger.info("Klassenstufe von %s: %s" % (user.username, update.message.text))
    user.klasse = update.message.text
    logger.info(user.klasse)
    haupt_keyboard = [['Eine Frage stellen'],
                      ['Eine Frage beantworten']]
    update.message.reply_text('Was möchtest du tun?', reply_markup=ReplyKeyboardMarkup(haupt_keyboard, one_time_keyboard=True))

    return FRAGE


def frage(bot, update):
    user = update.message.from_user
    if update.message.text == 'Eine Frage stellen':
        fach_keyboard = [['Mathe','Deutsch'],
                         ['Englisch','Physik'],
                         ['Chemie','Biologie'],
                         ['Geschichte','Erdkunde'],
                         ['Musik','BK']]
        update.message.reply_text('In welchem Fach möchtest du etwas fragen?', reply_markup=ReplyKeyboardMarkup(fach_keyboard, one_time_keyboard=True))
        return FRAGEN
    elif update.message.text == 'Eine Frage beantworten':
        bot.sendMessage(chat_id=update.message.chat_id, text='Aktuelle Fragen:')
        bot.sendMessage(chat_id=update.message.chat_id, text='1)\nFach: Mathe\nKlasse: 12\nFrage: Was ist 1+1?')
        bot.sendMessage(chat_id=update.message.chat_id, text='2)\nFach: Geschichte\nKlasse: 10\nFrage: Wer war Napoleon?')
        bot.sendMessage(chat_id=update.message.chat_id, text='3)\nFach: Informatik\nKlasse: 11\nFrage: Was ist ein Array?')
        fragen_keyboard = [['1','2','3'],
                           ['Vorherige Fragen','Nächste Fragen']]

        update.message.reply_text('Wähle, welche Frage du beantworten möchtest:', reply_markup=ReplyKeyboardMarkup(fragen_keyboard, one_time_keyboard=True))
        return BEANTWORTEN

    return ConversationHandler.END

def fragen(bot, update):
    global fragfach
    fragfach = update.message.text
    update.message.reply_text('Wie lautet deine Frage?')
    return HAUPTMENUE

def beantworten(bot, update):
    if update.message.text == '1':
        bot.sendMessage(chat_id=update.message.chat_id, text='1)\nFach: Mathe\nKlasse: 12\nFrage: Was ist 1+1?')
        bot.sendMessage(chat_id=update.message.chat_id, text='Schreibe bitte deine Antwort:')
        return HAUPTMENUE
    else:
        return HAUPTMENUE

def hauptmenue(bot, update):
    user = update.message.from_user
    bot.sendMessage(chat_id=update.message.chat_id, text='Deine Frage/Antwort wurde gespeichert')
    haupt_keyboard = [['Eine Frage stellen'],
                      ['Eine Frage beantworten']]
    update.message.reply_text('Was möchtest du tun?',
                              reply_markup=ReplyKeyboardMarkup(haupt_keyboard, one_time_keyboard=True))
    return FRAGE

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)

    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater("Hier Bot-Token einsetzen")

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            KLASSE: [RegexHandler('\d', klasse)],
            FRAGE: [MessageHandler(Filters.all, frage)],
            FRAGEN: [MessageHandler(Filters.all, fragen)],
            HAUPTMENUE: [MessageHandler(Filters.all, hauptmenue)],
            BEANTWORTEN: [MessageHandler(Filters.all, beantworten)]

        },

        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )

    dp.add_handler(conv_handler)

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

