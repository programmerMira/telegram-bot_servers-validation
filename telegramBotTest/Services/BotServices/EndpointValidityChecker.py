import requests

class EndpointValidityCheacker(object):
    """ Class for checking endpoint`s validiry (returns True if reply is 200) """

    def Check(self, endpoint):
        try:
            if not endpoint.startswith('http://'):
                endpoint = '{}{}'.format('http://',endpoint)
            result = requests.get(endpoint)
            if result.status_code == 200:
                return True
            return False
        except Exception as e:
            print("EndpointValidityCheacker Exception Check: ",e)
            return False