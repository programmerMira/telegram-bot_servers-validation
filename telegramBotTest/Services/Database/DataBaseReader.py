class DataBaseReader(object):
    
    def __init__(self, connection):
        self.__connection = connection

    def ReadAll(self):
        result = None
        try:
            with self.__connection.Connection.cursor() as cursor:
                cursor.execute(self.__queryGet)
                result = cursor.fetchall()
        except Exception as e:
            print(e)
        
        return result

    def ReadEndpoints(self, chat_id):
        result = None
        try:
            with self.__connection.Connection.cursor() as cursor:
                cursor.execute(self.__queryGetEndpoints)
                result = cursor.fetchall()
        except Exception as e:
            print(e)
        
        return result

    __connection = None
    __queryGet = "SELECT name FROM endpoints;"
    __queryGetEndpoints = "SELECT name FROM endpoints WHERE id = (SELECT endpoint_id FROM chat_endpoints WHERE chat_id = {} LIMIT 1);"