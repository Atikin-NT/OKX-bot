import json
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
    parser = Logic(apikey, secretkey, passphrase)
    parser.funding_account()
    # parser.earn_account()
    return
    with open("res.json", "w") as file:
        json.dump(response_json, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    CreateTable().execute()
    main()
