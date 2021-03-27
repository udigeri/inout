import requests

class Restful():
    def __init__(self):
        pass

    def _request(self, method, url, data):
        response = None
        if data == None:
            try:
                response = requests.request(method, url=url)
            except Exception as err:
                print(err)
        else:
            try:
                response = requests.request(method, 
                                            url=url, 
                                            data=data, 
                                            headers={'Content-Type':'application/json'} )
            except Exception as err:
                print(err)
        return response

    def get(self, endpoint, data=None):
        return self._request("get", endpoint, data)

    def post(self, endpoint, data=None):
        return self._request("post", endpoint, data)

    def put(self, endpoint, data=None):
        return self._request("put", endpoint, data)

    def delete(self, endpoint, data=None):
        return self._request("delete", endpoint, data)