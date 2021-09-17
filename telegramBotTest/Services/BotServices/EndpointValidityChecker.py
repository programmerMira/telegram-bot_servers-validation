import requests

class EndpointValidityCheacker(object):

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