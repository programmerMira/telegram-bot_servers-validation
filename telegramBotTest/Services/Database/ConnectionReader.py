from Exceptions.LoseConnectionFileException import LoseConnectionFileException
import os

class ConnectionReader(object):
    """ Class for reading file Connections/Connection.json """

    def Read(self):
        if(not os.path.exists(self.__configPath)):
            raise LoseConnectionFileException(self.__fileException, str(type(self).__name__))
        with(open(self.__configPath, 'r')) as file:
            return file.read()


    __configPath = os.path.dirname(os.path.abspath(__file__)).replace("/Services/Database", "/Connections/Connection.json")
    __fileException = "Отсутсвует файл подключения по пути: {0}".format(os.path.dirname(os.path.abspath(__file__)).replace("/Services/Database", "/Connections/Connection.json"))