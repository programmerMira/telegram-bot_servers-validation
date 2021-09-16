class DataBaseReader(object):
    
    def __init__(self, connection):
        self.__connection = connection

    def ReadAllEndpoints(self):
        result = None
        try:
            with self.__connection.Connection.cursor() as cursor:
                cursor.execute(self.__queryGetEndpoints)
                result = cursor.fetchall()
        except Exception as e:
            print("DataBaseReader Exception ReadAllEndpoints: ",e)
        
        return result

    def ReadAllChats(self):
        result = None
        try:
            with self.__connection.Connection.cursor() as cursor:
                cursor.execute(self.__queryGetChats)
                result = cursor.fetchall()
        except Exception as e:
            print("DataBaseReader Exception ReadAllChats: ",e)
        
        return result

    def ReadEndpointsForChat(self, chat_id):
        result = None
        try:
            with self.__connection.Connection.cursor() as cursor:
                cursor.execute(self.__queryGetChatId.format(str(chat_id)))
                id = cursor.fetchone()
                if not id:
                    return result
                id=id[0]
                cursor.execute(self.__queryGetEndpointsForChat.format(str(id)))
                result = cursor.fetchall()
        except Exception as e:
            print("DataBaseReader Exception ReadEndpointsForChat: ",e)
        
        return result

    __connection = None
    __queryGetEndpoints = "SELECT name FROM endpoints;"
    __queryGetChats = "SELECT chat_id FROM chats;"
    __queryGetChatId = "SELECT id FROM chats WHERE chat_id='{}' LIMIT 1;"
    __queryGetEndpointsForChat = "SELECT name FROM endpoints INNER JOIN chat_endpoints ON endpoints.id = chat_endpoints.endpoint_id WHERE chat_endpoints.chat_id={};"