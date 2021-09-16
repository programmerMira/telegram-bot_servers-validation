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
                cursor.execute(self.__queryGetEndpointsForChat)
                result = cursor.fetchall()
        except Exception as e:
            print("DataBaseReader Exception ReadEndpointsForChat: ",e)
        
        return result

    __connection = None
    __queryGetEndpoints = "SELECT name FROM endpoints;"
    __queryGetChats = "SELECT chat_id FROM chats;"
    __queryGetEndpointsForChat = "SELECT name FROM endpoints WHERE id = (SELECT endpoint_id FROM chat_endpoints WHERE chat_id = {} LIMIT 1);"