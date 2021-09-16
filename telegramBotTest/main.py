import telebot
from telebot import types
import time

from Services.BotServices.JsonParser import JsonParser
from Services.BotServices.ConfigReader import ConfigReader

from Connections.DataBaseConnection import DataBaseConnection
from Services.Database.ConnectionReader import ConnectionReader
from Services.Database.DataBaseReader import DataBaseReader
from Services.Database.DataBaseUpdater import DataBaseUpdater
from Services.Database.DataBaseWriter import DataBaseWriter
from Services.Database.DataBaseDeleter import DataBaseDeleter

#region variables
jsonParser = JsonParser()

connectionReader = ConnectionReader()
connection = jsonParser.Pars(connectionReader.Read())
databaseConnection = DataBaseConnection(connection)

configReader = ConfigReader()
config = jsonParser.Pars(configReader.Read())

databaseReader = DataBaseReader(databaseConnection)
databaseUpdater = DataBaseUpdater(databaseConnection)
databaseWriter = DataBaseWriter(databaseConnection)
databaseDeleter = DataBaseDeleter(databaseConnection)
#endregion

bot = telebot.TeleBot(config["HttpApiToken"])

#welcome message
@bot.message_handler(commands=['start'])
def welcome(message):
    #keyboard
    markup = types.InlineKeyboardMarkup(row_width=3)
    item1 = types.InlineKeyboardButton("Список точек",callback_data="watch")
    item2 = types.InlineKeyboardButton("Добавить",callback_data="add")
    item3 = types.InlineKeyboardButton("Удалить",callback_data="delete")
    
    markup.add(item1,item2,item3)
    
    bot.send_message(message.chat.id, "Привет, {0.first_name}!\nЯ бот - <b>{1.first_name}</b>\nМоя работа - следить за активностью указанных вами точек/серверов/сайтов!".format(message.from_user, bot.get_me()), parse_mode="html", reply_markup=markup)

#inline menu relies
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'start':
                markup = types.InlineKeyboardMarkup(row_width=3)
                item1 = types.InlineKeyboardButton("Список точек",callback_data="watch")
                item2 = types.InlineKeyboardButton("Добавить",callback_data="add")
                item3 = types.InlineKeyboardButton("Удалить",callback_data="delete")
                markup.add(item1,item2,item3)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Привет, {0.first_name}!\nЯ бот - <b>{1.first_name}</b>\nМоя работа - следить за активностью указанных вами точек/серверов/сайтов!".format(call.message.from_user, bot.get_me()) , parse_mode="html", reply_markup=markup)
            elif call.data == 'watch':
                keyboard = types.InlineKeyboardMarkup(row_width=3)
                add = types.InlineKeyboardButton(text="Добавить", callback_data="add")
                delete = types.InlineKeyboardButton(text="Удалить", callback_data="delete")
                back = types.InlineKeyboardButton(text="Назад", callback_data="start")
                keyboard.add(add,delete,back)
                #************GET FROM DATABASE**********************
                tmp_endpoints = databaseReader.ReadEndpointsForChat(call.message.chat.id)
                endpoints=[]
                for endpoint in tmp_endpoints:
                    endpoints.append('{} - {} - {}'.format(endpoint[0],endpoint[1], endpoint[2]))
                #***************************************************
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=endpoints, parse_mode="html",  reply_markup=keyboard)
            elif call.data == 'add':
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="You need to upload the file for the uniqueness check!")
            elif call.data == 'delete':
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                #************GET FROM DATABASE**********************
                a = types.InlineKeyboardButton(text="Точка 1", callback_data="Точка 1")
                b = types.InlineKeyboardButton(text="Точка 2", callback_data="Точка 2")
                c = types.InlineKeyboardButton(text="Точка 3", callback_data="Точка 3")
                #***************************************************
                z = types.InlineKeyboardButton(text="Назад", callback_data="start")
                keyboard.add(a,b,c,z)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите ту точку, что хотите удалить:", reply_markup=keyboard)
            else:
                #************DELETE POINT FROM DATABASE*************
                pass
                #***************************************************
    except Exception as e:
        print(repr(e))


#RUN
while True:
    try:
        print("[*] bot starting..")
        #bot.send_message(owner, "[*] bot starting..")
        print("[*] bot started!")
        #bot.send_message(owner, "[*] bot started!")
        bot.polling(none_stop=True, interval=2)
        # Предполагаю, что бот может мирно завершить работу, поэтому
        # даем выйти из цикла
        break

    except Exception as ex:
        print("[*] error - {}".format(str(ex))) # Описание ошибки
        #bot.send_message(owner, "[*] error - {}".format(str(ex)))
        print("[*] rebooting..")
        #bot.send_message(owner, "[*] rebooting..")
        bot.stop_polling()
        # Останавливаем чтобы не получить блокировку
        time.sleep(15)
        print("[*] restarted!")
        #bot.send_message(owner, "[*] restarted!")