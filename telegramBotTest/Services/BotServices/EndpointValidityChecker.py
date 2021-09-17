import requests

class EndpointValidityCheacker(object):

    def Check(self, endpoint):
        try:
            result = requests.get(endpoint)
            if result.status_code == 200:
                return True
            return False
        except Exception as e:
            print("EndpointValidityCheacker Exception Check: ",e)
            return False