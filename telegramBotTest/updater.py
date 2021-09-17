#updates endpoints every 15 minutes
#region imports
import schedule
import time

from Connections.DataBaseConnection import DataBaseConnection
from Services.BotServices.JsonParser import JsonParser
from Services.BotServices.ConfigReader import ConfigReader
from Services.BotServices.EndpointValidityChecker import EndpointValidityCheacker
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

endpointValidityCheck = EndpointValidityCheacker()

databaseReader = DataBaseReader(databaseConnection)
databaseUpdater = DataBaseUpdater(databaseConnection)
databaseWriter = DataBaseWriter(databaseConnection)
databaseDeleter = DataBaseDeleter(databaseConnection)
#endregion

#region debug area: test con. to db
#input must be chat id, e.g. "-536304400"
"""
chatID = "-536304400"
databaseWriter.WriteChat(chatID)
databaseWriter.WriteEndpointAndChat([chatID, "www.vk.com", "vk main page", endpointValidityCheck.Check("www.vk.com")])

res=databaseReader.ReadAllEndpoints()
print(res)

other_res = databaseReader.ReadEndpointsForChat("-536304400")
print(other_res)

chats=databaseReader.ReadAllChats()
print(chats)

databaseUpdater.UpdateEndpointStateAndDescription(["-536304400","www.facebook.com","Facebook main page", True])

res=databaseReader.ReadAllEndpoints()
print(res)

other_res = databaseReader.ReadEndpointsForChat("-536304400")
print(other_res)
"""
#endregion

#region logic
def update():
    endpoints = databaseReader.ReadAllEndpoints()
    for endpoint in endpoints:
        validity = endpointValidityCheck.Check(endpoint[0])
        databaseUpdater.UpdateEndpointState([endpoint[0],validity])
        print("Updated: endpoint: {} with state: {}".format(endpoint[0],validity))

schedule.every(1).minutes.do(update)

while True:
    schedule.run_pending()
    time.sleep(1)

#endregion