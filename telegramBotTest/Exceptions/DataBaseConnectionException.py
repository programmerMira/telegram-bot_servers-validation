class DataBaseConnectionException(Exception):
    
    def __init__(self, message, className):
        self.__message = "Exception code: 000001. Ошибка сгенерирована классом {}. Message: {}".format(className, message)