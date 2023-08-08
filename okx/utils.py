import hmac
import base64
import datetime
from . import consts as c


def sign(message: str, secret_key: str) -> bytes:
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return base64.b64encode(d)


def pre_hash(timestamp: str, method: str, request_path: str, body: str)-> str:
    """
    Предварительный хэш
    """
    return str(timestamp) + str.upper(method) + request_path + body


def get_header(api_key: str, sign: bytes, timestamp: str, passphrase: str) -> dict:
    header = dict()
    header[c.CONTENT_TYPE] = c.APPLICATION_JSON
    header[c.OK_ACCESS_KEY] = api_key
    header[c.OK_ACCESS_SIGN] = sign
    header[c.OK_ACCESS_TIMESTAMP] = str(timestamp)
    header[c.OK_ACCESS_PASSPHRASE] = passphrase
    return header

def get_header_no_sign() -> dict:
    header = dict()
    header[c.CONTENT_TYPE] = c.APPLICATION_JSON
    return header

def parse_params_to_str(params: dict) -> str:
    url = '?'
    for key, value in params.items():
        if(value != ''):
            url = url + str(key) + '=' + str(value) + '&'
    url = url[0:-1]
    return url


def get_timestamp() -> str:
    """
    Получаем текущее время
    """
    now = datetime.datetime.utcnow()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"


def signature(timestamp: str, method: str, request_path: str, body: str, secret_key: str) -> bytes:
    if str(body) == '{}' or str(body) == 'None':
        body = ''
    message = str(timestamp) + str.upper(method) + request_path + str(body)

    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()

    return base64.b64encode(d)