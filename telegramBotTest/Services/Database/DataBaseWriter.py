
class DataBaseWriter(object):
    
    def __init__(self, connection):
        self.__connection = connection

    def WriteChat(self, data):
        with self.__connection.Connection.cursor() as cursor:
            pass
    
    def WriteEndpointAndChat(self, data):
        with self.__connection.Connection.cursor() as cursor:
            pass
    
    __connection = None

    __insertChat = "INSERT INTO chats VALUES () ON CONFLICT DO NOTHING;"
    __insertEndpoint = "INSERT INTO endpoints VALUES () ON CONFLICT DO NOTHING;"
    __insertChatEndpointBond = "INSERT INTO chat_endpoints VALUES () ON CONFLICT DO NOTHING;"