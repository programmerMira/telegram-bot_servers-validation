#updates endpoints every config["TimeStampBetweenRequests"] minutes

#region imports
import schedule
import time

from Services.BotServices.JsonParser import JsonParser

from Services.BotServices.ConfigReader import ConfigReader
from Services.Database.ConnectionReader import ConnectionReader

from Connections.DataBaseConnection import DataBaseConnection
from Services.Database.DataBaseReader import DataBaseReader
from Services.Database.DataBaseUpdater import DataBaseUpdater

from Services.BotServices.EndpointValidityChecker import EndpointValidityCheacker
#endregion

#region variables
jsonParser = JsonParser()

configReader = ConfigReader()
config = jsonParser.Pars(configReader.Read())

connectionReader = ConnectionReader()
connection = jsonParser.Pars(connectionReader.Read())

databaseConnection = DataBaseConnection(connection)
databaseReader = DataBaseReader(databaseConnection)
databaseUpdater = DataBaseUpdater(databaseConnection)

endpointValidityCheck = EndpointValidityCheacker()
#endregion

#region logic
def update():
    try:
        endpoints = databaseReader.ReadAllEndpoints()
        for endpoint in endpoints:
            validity = endpointValidityCheck.Check(endpoint[0])
            databaseUpdater.UpdateEndpointState([endpoint[0],validity])
            print("Updated: endpoint: {} with state: {}".format(endpoint[0],validity))
    except Exception as e:
        print("updater.py update():",e)

schedule.every(int(config["TimeStampBetweenRequests"])).minutes.do(update)

while True:
    schedule.run_pending()
    time.sleep(1)

#endregion