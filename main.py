import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

with open("cities.json", "r", encoding='UTF-8') as read_file:
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


def get_last_letter(town: str):
    for i in range(len(town) - 1, -1, -1):
        if town[i] != 'Ъ' and town[i] != 'Ь' and town[i] != 'Ы':
            return town[i]


def start_command(update: Update, _: CallbackContext):
    update.effective_chat.send_message(text='Здравствуйте, это бот для игры в города! Напишите город и начнем игру!')


def get_town_from_user(update: Update, _: CallbackContext):
    global last_town_bot

    town = update.effective_message.text.upper()

    print(last_town_bot, town)
    if town in used_cities:
        update.effective_chat.send_message(text='Ха,попались! Такой город уже был! '
                                                'Напишите новый и мы продолжим игру!.')
    elif not is_exists_town(town):
        update.effective_chat.send_message(text='Кажется,вы написали несуществующий город. Пожалуйста, напишите новый!')
    elif last_town_bot == "" or get_last_letter(last_town_bot) == town[0]:
        print(get_last_letter(town))
        bot_town = get_town_by_letter(get_last_letter(town))
        update.effective_chat.send_message(text=bot_town)
        last_town_bot = bot_town.upper()

        used_cities.append(town)
        used_cities.append(bot_town)
    else:
        update.effective_chat.send_message(text='Извините, такой город не подходит. '
                                                'Напишите новый и мы продолжим игру!')


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
    with open('token.txt', 'r') as token:
        main(token.read())
