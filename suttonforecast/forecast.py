# Forecast Bot
## Director of the whole process, everything goes by him
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, CallbackQueryHandler

from . import __version__
from .journalist import Journalist
from .towncrier import Towncrier
from .designer import Designer

from io import BytesIO
import logging
from datetime import time
from os import environ

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class Forecast:
    def __init__(self, BOT_KEY, CHANNEL_ID, ADMIN_ID, TIME_HOUR, TIME_MIN):
        self.BOT_KEY = BOT_KEY
        self.CHANNEL_ID = CHANNEL_ID
        self.ADMIN_ID = ADMIN_ID
        self.TIME = {
            "hours":int(TIME_HOUR),
            "minutes":int(TIME_MIN)
        }

        self.updater = Updater(token=self.BOT_KEY, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.jobqueue = self.updater.job_queue

        self.data = Journalist().data
        self.towncrier = Towncrier(self.updater, self.dispatcher, self.addCommand)


        def start(update, context):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Starting....!")
        self.addCommand("start", start)
        
        def help_needed(update, context):
            self.towncrier.tell(chatid=update.effective_chat.id, data="/dme: Envoie le Rapport Quotidien en privé\n/forcedme: /dme mais au Channel (ADMIN seulement)\n/version: Version actuelle")
        self.addCommand("help", help_needed)
        
        def version(update, context):
            self.towncrier.tell(chatid=update.effective_chat.id, data=f"Version {__version__}")
        self.addCommand("version", version)


        self.info_keyboard = [[InlineKeyboardButton("Liste des chalets", callback_data='chalet'),
                                InlineKeyboardButton("Liste des remontées", callback_data='remontee')],
                            [InlineKeyboardButton("Liste des pistes", callback_data='piste')]]
        self.info_keyboard_markup = InlineKeyboardMarkup(self.info_keyboard)

        def button(update, context):
            query = update.callback_query
            data = Designer().statutMessage(self.data, query.data)
            query.edit_message_text(text=data, reply_markup=self.info_keyboard_markup, parse_mode="Markdown")
        self.dispatcher.add_handler(CallbackQueryHandler(button))


        def dme(update, context):
            self.sendDailyMessage(update.effective_chat.id)
        self.addCommand("dme", dme)

        def forcedme(update, context):
            self.sendDailyMessage(self.CHANNEL_ID)
            self.towncrier.tell(self.ADMIN_ID, "Le Rapport Quotidien a été envoyé au groupe.")
        self.dispatcher.add_handler(CommandHandler("forcedme", forcedme, filters=Filters.user(user_id=int(self.ADMIN_ID))))

        def sendWebcams(update, context):
            self.webcams_bytes = Journalist.getWebcamImages()
            self.towncrier.show(update.effective_chat.id, self.webcams_bytes)
        self.addCommand("webcam", sendWebcams)

        def automaticDailyMessage(context):
            self.sendDailyMessage(self.CHANNEL_ID)
        self.jobqueue.run_daily(automaticDailyMessage, time(hour=self.TIME["hours"], minute=self.TIME["minutes"]))


        def error(update, context):
            logging.warning(f'Update {update} caused error {context.error}')
        self.dispatcher.add_error_handler(error)

        def unknown(update, context):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Désolé, cette commande n'a pas été reconnue.")
        unknown_handler = MessageHandler(Filters.command, unknown)
        self.dispatcher.add_handler(unknown_handler)

        self.updater.start_polling()
        self.updater.idle()
    
    def showInlineKeyboard(self, chatid):
        self.dispatcher.bot.send_message(chat_id=chatid, text="Souhaitez-vous d'autres informations?", reply_markup=self.info_keyboard_markup)

    def sendDailyMessage(self, channelid):
        # Scrape info
        self.data = Journalist().data
        # Prepare Info
        data_designed = Designer().dailyMessage(self.data)
        # Send info
        for m in data_designed:
            self.towncrier.tell(channelid, m)
        # Get the combined webcam images in BytesIO
        self.webcams_bytes = Journalist.getWebcamImages()
        self.towncrier.show(channelid, self.webcams_bytes)
        self.showInlineKeyboard(channelid)

    def addCommand(self, keyword, function):
        self.dispatcher.add_handler(CommandHandler(keyword, function))