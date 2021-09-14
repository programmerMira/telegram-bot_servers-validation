#updates endpoints every 15 minutes
#region imports
from Connections.DataBaseConnection import DataBaseConnection
from Services.BotServices.JsonParser import JsonParser
from Services.BotServices.ConfigReader import ConfigReader
from Services.Database.ConnectionReader import ConnectionReader
from Services.Database.DataBaseReader import DataBaseReader
from Services.Database.DataBaseUpdater import DataBaseUpdater
#endregion

#region variables
jsonParser = JsonParser()

connectionReader = ConnectionReader()
connection = jsonParser.Pars(connectionReader.Read())
databaseConnection = DataBaseConnection(connection)

configReader = ConfigReader()
config = jsonParser.Pars(configReader.Read())

databaseReader = DataBaseReader(databaseConnection)
databaseUpdater = DataBaseUpdater(databaseConnection)
#endregion

#region logic

#endregion