# Towncrier bot
## Yells messages to people
from telegram.ext import Updater, CommandHandler


class Towncrier:
    def __init__(self, updater, dispatcher, addCommand):
        self.updater = updater
        self.dispatcher = dispatcher
        self.addCommand = addCommand
        self.setKeyWords()

    def setKeyWords(self):
        def start(update, context):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Stating....!")
        self.addCommand("start", start)
    
    def tell(self, chatid, data):
        self.dispatcher.bot.send_message(chat_id=chatid, text=data, parse_mode="Markdown")
    
    def show(self, chatid, data):
        self.dispatcher.bot.send_photo(chatid, photo=data)