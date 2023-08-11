import time
from logic.logic import Logic
from db.idb import CreateTable
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
okx_config = config['okx']

apikey = okx_config['apikey']
secretkey = okx_config['secretkey']
passphrase = okx_config['passphrase']

def main():
    """
    Оказалосб, что существует какое-то ограничение на ордера.
    Мне не удалось узнать, где можно посмотреть этот лимит. Даже 
    задержки по времени не помогли.

    Но это первый проект с довольно чистым кодом)
    """
    logic = Logic(apikey, secretkey, passphrase)

    while True:
        logic.funding_account()
        logic.earn_acc()
        time.sleep(60 *60 * 24)

if __name__ == "__main__":
    CreateTable().execute()
    main()
