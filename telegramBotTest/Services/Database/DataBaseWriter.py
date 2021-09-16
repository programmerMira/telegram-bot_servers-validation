from datetime import datetime

class DataBaseWriter(object):
    """ Class that works with database: insert-queries """

    def __init__(self, connection):
        self.__connection = connection

    def WriteChat(self, data):
        """
            Writes chat_id to db if not exists
            data => chat_id
        """
        try:
            with self.__connection.Connection.cursor() as cursor:
                cursor.execute(self.__insertChat.format(str(data),str(datetime.now())))
        except Exception as e:
            print("DataBaseWriter Exception WriteChat: ",e)
    
    def WriteEndpointAndChat(self, data):
        """
            Writes endpoint and chat_endpoint if not exists
            data => [chat_id, endpoint_name, endpoint_description, endpoint_state]
        """
        try:
            with self.__connection.Connection.cursor() as cursor:
                cursor.execute(self.__insertEndpoint.format(str(data[1]),str(data[2]),str(data[3]),str(datetime.now())))
            
            with self.__connection.Connection.cursor() as cursor:
                cursor.execute(self.__selectFromChats.format(str(data[0])))
                chat_id = cursor.fetchone()
                if chat_id:
                    chat_id=chat_id[0]
                
                cursor.execute(self.__selectFromEndpoints.format(str(data[1])))
                endpoint_id = cursor.fetchone()
                if endpoint_id:
                    endpoint_id=endpoint_id[0]
                
                if chat_id and endpoint_id:
                    cursor.execute(self.__selectFromChatEndpoints.format(str(chat_id),str(endpoint_id)))
                    chat_endpoint_id = cursor.fetchone()
                    if chat_endpoint_id:
                        chat_endpoint_id=chat_endpoint_id[0]
                    if not chat_endpoint_id:
                        cursor.execute(self.__insertChatEndpointBond.format(str(chat_id),str(endpoint_id),str(datetime.now())))
        except Exception as e:
            print("DataBaseWriter Exception WriteEndpointAndChat: ",e)
    
    __connection = None

    __insertChat = "INSERT INTO chats(chat_id, created_at) VALUES ('{}', '{}') ON CONFLICT DO NOTHING;"
    __insertEndpoint = "INSERT INTO endpoints(name, description, state, created_at) VALUES ('{}','{}',{},'{}') ON CONFLICT DO NOTHING;"
    __insertChatEndpointBond = "INSERT INTO chat_endpoints(chat_id, endpoint_id, created_at) VALUES ({},{},'{}') ON CONFLICT DO NOTHING;"

    __selectFromChats = "SELECT id FROM chats WHERE chat_id='{}' LIMIT 1;"
    __selectFromEndpoints = "SELECT id FROM endpoints WHERE name='{}' LIMIT 1;"
    __selectFromChatEndpoints = "SELECT id FROM chat_endpoints WHERE chat_id={} AND endpoint_id={} LIMIT 1;"