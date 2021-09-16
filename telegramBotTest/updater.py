#updates endpoints every 15 minutes
#region imports
from Connections.DataBaseConnection import DataBaseConnection
from Services.BotServices.JsonParser import JsonParser
from Services.BotServices.ConfigReader import ConfigReader
from Services.Database.ConnectionReader import ConnectionReader
from Services.Database.DataBaseReader import DataBaseReader
from Services.Database.DataBaseUpdater import DataBaseUpdater
from Services.Database.DataBaseWriter import DataBaseWriter
from Services.Database.DataBaseDeleter import DataBaseDeleter
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
databaseWriter = DataBaseWriter(databaseConnection)
databaseDeleter = DataBaseDeleter(databaseConnection)
#endregion

#region debug area: test con. to db
#input must be chat id, e.g. "-536304400"
chatID = "-536304401"
databaseWriter.WriteChat(chatID)
databaseWriter.WriteEndpointAndChat([chatID, "www.facebook.com", "Facebook main page", True])

res=databaseReader.ReadAllEndpoints()
print(res)

other_res = databaseReader.ReadEndpointsForChat("-536304400")
print(other_res)
#endregion

#region logic

#endregion