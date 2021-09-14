
class DataBaseUpdater(object):
    
    def __init__(self, connection):
        self.__connection = connection

    def UpdateChat(self, data):
        with self.__connectionDO.Connection.cursor() as cursor:
            pass
    
    def UpdateEndpointAndChat(self, data):
        with self.__connectionDO.Connection.cursor() as cursor:
            pass
    
    __connection = None