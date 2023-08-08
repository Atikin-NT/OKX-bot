import json
import requests
from . import consts as c, utils


class Client():

    def __init__(self, api_key: str, api_secret_key: str, passphrase: str, base_api = c.API_URL):
        self.API_KEY = api_key
        self.API_SECRET_KEY = api_secret_key
        self.PASSPHRASE = passphrase
        self.domain = base_api

    def _request(self, method: str, request_path: str, params: dict) -> any:
        if method == "GET":
            request_path = request_path + utils.parse_params_to_str(params)
        timestamp = utils.get_timestamp()

        body = json.dumps(params) if method == "POST" else ""
        sign = utils.sign(utils.pre_hash(timestamp, method, request_path, str(body)), self.API_SECRET_KEY)
        header = utils.get_header(self.API_KEY, sign, timestamp, self.PASSPHRASE)

        response = None
        if method == "GET":
            response = requests.get(url=self.domain + request_path, headers=header)
        elif method == "POST":
            response = requests.post(url=self.domain + request_path, data=body, headers=header)
        
        return response.json()

    def request_without_params(self, method: str, request_path: str) -> any:
        return self._request(method, request_path, {})

    def request_with_params(self, method: str, request_path: str, params: dict) -> any:
        return self._request(method, request_path, params)
