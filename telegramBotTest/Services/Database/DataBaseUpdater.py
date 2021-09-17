from datetime import datetime

class DataBaseUpdater(object):
    """ Class that works with database: update-queries """
    
    def __init__(self, connection):
        self.__connection = connection

    def UpdateEndpointState(self, data):
        """
            Updates info about endpoint
            data => [endpoint_name, endpoint_state]
        """
        try:
            with self.__connection.Connection.cursor() as cursor:
                cursor.execute(self.__queryUpdateEndpoint.format(str(data[1]),str(datetime.now()),str(data[0])))
        except Exception as e:
            print("DataBaseUpdater Exception UpdateEndpointState: ",e)

    __connection = None

    __queryUpdateEndpoint = "UPDATE endpoints SET state={}, updated_at='{}' WHERE name='{}';"