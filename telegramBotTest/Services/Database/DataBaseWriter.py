
class DataBaseWriter(object):
    
    def __init__(self, connection):
        self.__connection = connection

    def WriteChat(self, data):
        with self.__connectionDO.Connection.cursor() as cursor:
            pass
    
    def WriteEndpointAndChat(self, data):
        with self.__connectionDO.Connection.cursor() as cursor:
            pass
    
    __connection = None