from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler

def start_command(update: Update, _: CallbackContext):
    update.effective_chat.send_message(text=)


def main(token:str):
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start_command)


if __name__ == '__main__':
    main('5049350468:AAFKVzYmElqUZqO0aDoitV-ELnL4_czafBo')



