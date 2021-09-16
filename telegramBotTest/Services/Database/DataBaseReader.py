class DataBaseReader(object):
    """ Class that works with database: select-queries """
    def __init__(self, connection):
        self.__connection = connection

    def ReadAllEndpoints(self):
        """ Gets endpoints` information from the table 'endpoints' """
        result = None
        try:
            with self.__connection.Connection.cursor() as cursor:
                cursor.execute(self.__queryGetEndpoints)
                result = cursor.fetchall()
        except Exception as e:
            print("DataBaseReader Exception ReadAllEndpoints: ",e)
        
        return result

    def ReadAllChats(self):
        """ Gets chats` information from the table 'chats' """
        result = None
        try:
            with self.__connection.Connection.cursor() as cursor:
                cursor.execute(self.__queryGetChats)
                result = cursor.fetchall()
        except Exception as e:
            print("DataBaseReader Exception ReadAllChats: ",e)
        
        return result

    def ReadEndpointsForChat(self, chat_id):
        """ Gets information about endpoints related to specific chat (chat_id) """
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
    __queryGetEndpoints = "SELECT name, description, state FROM endpoints;"
    __queryGetChats = "SELECT chat_id FROM chats;"
    __queryGetChatId = "SELECT id FROM chats WHERE chat_id='{}' LIMIT 1;"
    __queryGetEndpointsForChat = "SELECT name, description, state FROM endpoints INNER JOIN chat_endpoints ON endpoints.id = chat_endpoints.endpoint_id WHERE chat_endpoints.chat_id={};"