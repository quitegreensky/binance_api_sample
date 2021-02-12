import requests
import hashlib
import hmac


class BinanceAPI:

    def __init__(self, apiKey: str, secretKey: str):
        self.baseAddress = "https://api.binance.com"
        self.apiKey = apiKey
        self.secretKey = secretKey
        self.recvWindow = 50000

    def _fetch(self, url: str, method: str):
        """
        sends request to given url
        """
        if method=="GET":
            req = requests.get
        elif method=="POST":
            req = requests.post
        else:
            raise TypeError("Invalid method type %s"%method)

        response = req(url, headers={"X-MBX-APIKEY":self.apiKey})
        return response

    def _add_parameter(self, parameter_dic)->str:
        """
        converts a dictionary of parameters to
        a query string
        """
        link = ""
        for parameter, value in parameter_dic.items():
            if not value:
                continue
            parameter= parameter.replace(' ','')
            value= str(value).replace(' ','')
            link= link+'&'+parameter+'='+value
        return link[1:]

    def _sign(sel, message, secret)->str:
        """
        HMAC-SHA256 signature method
        """
        signature = hmac.new(
            bytes(secret.encode("utf-8")),
            msg=message.encode("utf-8"),
            digestmod=hashlib.sha256
        ).hexdigest().upper()
        return signature.lower()

    def _merge_address(self,endpoint, parameters='')->str:
        """
        merges base address, endpoint and given query for parameters
        """
        return self.baseAddress+endpoint+"?"+ parameters

    def getTimestamp(self)->str:
        """
        returns server time
        """
        time = self.serverTime()
        if not time:
            return False
        return time.json()["serverTime"]

    def serverTime(self)->requests:
        """
        Gets the sever time and returns request object
        """
        endpoint = "/api/v3/time"
        url = self._merge_address(endpoint)
        response = self._fetch(url, "GET")
        return response

    def _secure_url(self, params={})->str:
        """
        adds recvWinodw and timestamp to parameters
        and then adds signature.use only if request
        needs HMAC-SHA256 signature.
        """
        params["recvWindow"] = self.recvWindow
        params["timestamp"] = self.getTimestamp()
        query = self._add_parameter(parameter_dic=params)
        params["signature"] = self._sign(query, self.secretKey)
        query = self._add_parameter(parameter_dic=params)
        return query

    def getAll(self, params)->requests:
        endpoint = "/sapi/v1/capital/config/getall"
        params = self._secure_url(params)
        url = self._merge_address(endpoint, params)
        response = self._fetch(url, "GET")
        return response