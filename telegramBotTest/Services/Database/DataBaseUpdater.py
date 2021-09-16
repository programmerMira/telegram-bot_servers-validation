from datetime import datetime

class DataBaseUpdater(object):
    """ Class that works with database: update-queries """
    
    def __init__(self, connection):
        self.__connection = connection

    def UpdateEndpointStateAndDescription(self, data):
        """
            Updates info about endpoint
            data => [chat_id, endpoint_name, endpoint_description, endpoint_state]
        """
        try:
            with self.__connection.Connection.cursor() as cursor:
                cursor.execute(self.__queryUpdateEndpoint.format(str(data[2]),str(data[3]),str(datetime.now()),str(data[1])))
        except Exception as e:
            print("DataBaseUpdater Exception UpdateEndpointStateAndDescription: ",e)

    __connection = None

    __queryUpdateEndpoint = "UPDATE endpoints SET description='{}', state={}, updated_at='{}' WHERE name='{}';"