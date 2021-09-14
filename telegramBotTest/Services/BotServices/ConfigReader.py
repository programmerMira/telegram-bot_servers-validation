from Exceptions.LoseConfigFileException import LoseConfigFileException
import os

class ConfigReader(object):
    
    def __init__(self):
        pass

    def Read(self):
        if(not os.path.exists(self.__configPath)):
            raise LoseConfigFileException(self.__fileException, str(type(self).__name__))
        with(open(self.__configPath, 'r')) as file:
            return file.read()


    __configPath = os.path.dirname(os.path.abspath(__file__)).replace("\\Services\\BotServices", "\\Connections\\Config.json")
    __fileException = "Отсутсвует файл конфигурации по пути: {0}".format(os.path.dirname(os.path.abspath(__file__)).replace("\\Services\\BotServices", "\\Connections\\Config.json"))