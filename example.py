"""
from binance_api import BinanceAPI


class MyBinance(BinanceAPI):
    '''
    You can make your own custom requests
    if current ones does not satisfy you
    '''

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def mySecureRequest(self, parameter={}):
        '''
        let's assueme this request needs to be signed
        '''
        # if your request needs to be signed then use _secure_url()
        new_parameters = self._secure_url(parameter)

        # now make your url
        url = self._merge_address("your endpoint", new_parameters)

        # here is your respones to handle
        response = self._fetch(url, "GET")
        return response

    def myPublicRequest(self, parameter={}):

        # first make string of parameters
        new_parameters = self._add_parameter(parameter)

        # make url like this. give it an endpoint and string of parameters
        url = self._merge_address("/api/v3/time", new_parameters)

        # here is your response to handle
        respones = self._fetch(url, "GET")

        return respones


req = MyBinance("api key", "secret key")

res = req.myPublicRequest(parameter={"key": "value"})
print(res.text)
"""

from binance_api import BinanceAPI

apiKey = "api key"
secretKey = "secret key"

req = BinanceAPI(
    apiKey,
    secretKey
)

response = req.serverTime()
print(response.json())
