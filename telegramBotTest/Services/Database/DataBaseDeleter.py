
class DataBaseDeleter(object):
    
    def __init__(self, connection):
        self.__connection = connection

    def DeleteChat(self, data):
        """
            data => chat_id
        """
        try:
            with self.__connection.Connection.cursor() as cursor:
                cursor.execute(self.__queryDeleteChat.format(str(data)))
        except Exception as e:
            print("DataBaseDeleter Exception DeleteChat: ",e)

    def DeleteEndpoint(self, data):
        """
            data => endpoint_name
        """
        try:
            with self.__connection.Connection.cursor() as cursor:
                cursor.execute(self.__queryDeleteEndpoint.format(str(data)))
        except Exception as e:
            print("DataBaseDeleter Exception DeleteEndpoint: ",e)

    def DeleteChatEndpointBond(self, data):
        """
            data => [chat_id, endpoint_name]
        """
        try:
            with self.__connection.Connection.cursor() as cursor:
                cursor.execute(self.__queryDeleteChatEndpointBond.format(str(data[0]),str(data[1])))
        except Exception as e:
            print("DataBaseDeleter Exception DeleteChatEndpointBond: ",e)
    
    __connection = None
    __queryDeleteChat = "DELETE FROM chats WHERE chat_id='{}';"
    __queryDeleteEndpoint = "DELETE FROM endpoints WHERE name='{}';"
    __queryDeleteChatEndpointBond = "DELETE FROM chat_endpoints WHERE chat_id={} AND endpoint_id=(SELECT id FROM endpoint WHERE name='{}' LIMIT 1);"