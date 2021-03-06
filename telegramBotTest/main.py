#region imports
import telebot
from telebot import types
import time

from Services.BotServices.JsonParser import JsonParser
from Services.BotServices.ConfigReader import ConfigReader
from Services.BotServices.EndpointValidityChecker import EndpointValidityCheacker

from Connections.DataBaseConnection import DataBaseConnection
from Services.Database.ConnectionReader import ConnectionReader
from Services.Database.DataBaseReader import DataBaseReader
from Services.Database.DataBaseUpdater import DataBaseUpdater
from Services.Database.DataBaseWriter import DataBaseWriter
from Services.Database.DataBaseDeleter import DataBaseDeleter
#endregion

#region variables
jsonParser = JsonParser()

connectionReader = ConnectionReader()
connection = jsonParser.Pars(connectionReader.Read())
databaseConnection = DataBaseConnection(connection)

configReader = ConfigReader()
config = jsonParser.Pars(configReader.Read())

endpointValidityCheck = EndpointValidityCheacker()

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
    databaseWriter.WriteChat(message.chat.id)
    bot.send_message(message.chat.id, "Привет, {0.first_name}!\nЯ бот - <b>{1.first_name}</b>\nМоя работа - следить за активностью указанных вами точек/серверов/сайтов!".format(message.from_user, bot.get_me()), parse_mode="html", reply_markup=markup)

#addition handler
@bot.message_handler(commands=['add'])
def addition(message):
    try:
        endpoint_data = str(message.text).replace('/add','').strip()
        endpoint_name = endpoint_data[0:endpoint_data.find(' ')].strip()
        endpoint_description = endpoint_data[endpoint_data.find(' '):].strip()
        endpoint_state = endpointValidityCheck.Check(endpoint_name)
        if len(endpoint_name.strip())>0:
            databaseWriter.WriteEndpointAndChat([message.chat.id,endpoint_name,endpoint_description, endpoint_state])
        welcome(message)
    except Exception as e:
        bot.send_message(message.chat.id, "<i>Что-то пошло не так, пожалуста, проверьте првильность вводимой информации!</i>", parse_mode="html")
        welcome(message)

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
                endpoints=''
                for endpoint in tmp_endpoints:
                    if not endpoint[2]:
                        state="Не доступно"
                    else:
                        state="Доступно"
                    endpoints+='{} - {} - {}\n'.format(endpoint[0],endpoint[1], state)
                #***************************************************
                if endpoints=='':
                    endpoints='Тут пока пусто('
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=endpoints, parse_mode="html",  reply_markup=keyboard)
            elif call.data == 'add':
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                back = types.InlineKeyboardButton(text="Назад", callback_data="start")
                keyboard.add(back)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Для добавления нового сервера/ссылки введите сообщение следующего вида:\n<i>/add www.gmail.com Gmail Service</i>", parse_mode="html",  reply_markup=keyboard)
            elif call.data == 'delete':
                #************GET FROM DATABASE**********************
                tmp_endpoints = databaseReader.ReadEndpointsForChat(call.message.chat.id)
                btns=[]
                for endpoint in tmp_endpoints:
                    if not endpoint[2]:
                        state="Не доступно"
                    else:
                        state="Доступно"
                    btn_text = '{} - {} - {}\n'.format(endpoint[0],endpoint[1], state)
                    btns.append(types.InlineKeyboardButton(text=btn_text, callback_data='d-{}'.format(endpoint[0])))
                #***************************************************
                z = types.InlineKeyboardButton(text="Назад", callback_data="start")
                btns.append(z)
                keyboard = types.InlineKeyboardMarkup([btns])
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите ту точку, что хотите удалить:", reply_markup=keyboard)
            else:
                #************DELETE POINT FROM DATABASE*************
                if str(call.data).startswith('d-'):
                    databaseDeleter.DeleteChatEndpointBond([call.message.chat.id, str(call.data).replace('d-','')])
                else:
                    print("not delete",call.data)
                
                call.data='start'
                callback_inline(call)
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
