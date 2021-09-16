from Exceptions.DataBaseConnectionException import DataBaseConnectionException
import psycopg2

class DataBaseConnection():
    """  Class for connecting to database  
        
     Properties:
     Connection
    """

    def __init__(self, connection, autocommit=True):
        """  Creating connection """
        self.__dataBaseName = connection['DataBaseName']
        self.__dataBaseUser = connection['DataBaseUser']
        self.__dataBasePassword = connection['DataBasePassword']
        self.__dataBaseHost = connection['DataBaseHost']
        self.__dataBasePort = connection['DataBasePort']
        try:
            self.__connection = psycopg2.connect(dbname = self.__dataBaseName, user = self.__dataBaseUser, password = self.__dataBasePassword, host = self.__dataBaseHost, port = self.__dataBasePort)
            self.__connection.autocommit = autocommit
        except Exception as e:
            raise DataBaseConnectionException(self.__connectionErrorMessage+" : "+str(e), str(type(self).__name__))


    @property
    def Connection(self):
        """ Geting connection """
        return self.__connection

    def __del__(self):
        """ Close connection """
        self.__connection.close()

    __dataBaseName = ""
    __dataBaseUser = ""
    __dataBasePassword = ""
    __dataBaseHost = ""
    __dataBasePort = ""
    __connection = None
    __connectionErrorMessage = "Ошибка подлкючения к базе данных. Проверьте правильность введенных данных или соедение с сервером базы данных"