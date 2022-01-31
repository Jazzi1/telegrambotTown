import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

with open("cities.json", "r") as read_file:
    data = json.load(read_file)

cities = [i['name'] for i in data['city']]
used_cities = []
last_town_bot = ""


def is_exists_town(check_town: str):
    for town in cities:
        if town.upper() == check_town.upper():
            return True
    return False

def get_town_by_letter(first_letter: str):
    for town in cities:
        if town not in used_cities and town[0] == first_letter:
            return town
    return None

def start_command(update: Update, _: CallbackContext):
    update.effective_chat.send_message(text='Здравствуйте, это бот создан для игры в города! Напишите любой город и давайте анчнем игру!')


def get_town_from_user(update: Update, _: CallbackContext):
    global last_town_bot

    town = update.effective_message.text.upper()

    print(last_town_bot, town)
    if town in used_cities:
        update.effective_chat.send_message(text='Ха,попались! Такой город уже был! Напишите,пожалуйста, новый и мы продолжим игру!.')
    elif not is_exists_town(town):
        update.effective_chat.send_message(text='Кажется,вы написали несуществующий город. Пожалуйста, напишите новый и мы продолжим игру!')
    elif last_town_bot == "" or last_town_bot[-1] == town[0]:
        bot_town = get_town_by_letter(town[-1])
        update.effective_chat.send_message(text=bot_town)
        last_town_bot = bot_town.upper()

        used_cities.append(town)
        used_cities.append(bot_town)
    else:
        update.effective_chat.send_message(text='Извините, такой город не подходит. Напишите новый и мы продолжим игру!')


def main(token: str):
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start_command)
    get_town_from_user_handler = MessageHandler(Filters.text, get_town_from_user)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(get_town_from_user_handler)
    print(updater.bot.get_me())
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main('5049350468:AAFKVzYmElqUZqO0aDoitV-ELnL4_czafBo')



