# Forecast Bot
## Director of the whole process, everything goes by him
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)

from .journalist import *
from .towncrier import *
from .designer import *

from io import BytesIO
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class Forecast:
    def __init__(self, BOT_KEY, CHANNEL_ID):
        self.updater = Updater(token=BOT_KEY, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.CHANNEL_ID = CHANNEL_ID

        self.data = Journalist().data
        self.towncrier = Towncrier(self.updater, self.dispatcher, self.addCommand)


        def hello(update, context):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Hello!")
        self.addCommand("hello", hello)
        
        def journalist(update, context):
            context.bot.send_message(chat_id=update.effective_chat.id, text=self.data["info_time"])
        self.addCommand("journalist", journalist)

        def dme(update, context):
            self.sendDailyMessage()
        self.addCommand("dme", dme)

        self.updater.start_polling()
        self.updater.idle()
    
    def sendDailyMessage(self):
        # Scrape info
        self.data = Journalist().data
        data_designed = Designer().dailyMessage(self.data)
        for m in data_designed:
            self.towncrier.tell(self.CHANNEL_ID, m)

        self.webcams_image = Journalist.getWebcamImages()
        webcam_bytes = BytesIO()
        webcam_bytes.name = "webcams.jpeg"
        self.webcams_image.save(webcam_bytes, "JPEG")
        webcam_bytes.seek(0)
        self.towncrier.show(self.CHANNEL_ID, webcam_bytes)

    def askJournalist(self, update, context):
        print("hi")
        print(update, context)
        # context.bot.send_message(chat_id=update.effective_chat.id, text=self.data["info_time"])
        self.towncrier.tell(update, context, self.journalist.data["info-time"])
    
    def tellTowncrier(self, data):
        self.towncrier.tell(data)

    def addCommand(self, keyword, function):
        self.dispatcher.add_handler(CommandHandler(keyword, function))