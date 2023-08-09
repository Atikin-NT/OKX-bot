from logic.earn_acc import EarnAcc
from mock import MagicMock
from db.idb import AddCoin, ListCoin
import json
from pathlib import Path

RESOURCES_PATH = Path(__file__).parent.joinpath("data")

def inject_test_data(file):
    file = str(RESOURCES_PATH.joinpath(file))
    with open(file) as f:
        raw_data = json.load(f)
    return raw_data

# ------------- parse

def test_parse_empty():
    earn_acc = EarnAcc("api_key", "secret_key", "passphrase")
    response = inject_test_data('empty.json')
    earn_acc.account.get_earn_active = MagicMock()
    earn_acc.account.get_earn_active.return_value = response
    earn_acc.parse()

    assert earn_acc.earn_list == []

def test_parse_empty_three_coins():
    earn_acc = EarnAcc("api_key", "secret_key", "passphrase")
    response = inject_test_data('three_coin.json')
    earn_acc.account.get_earn_active = MagicMock()
    earn_acc.account.get_earn_active.return_value = response
    earn_acc.parse()

    assert earn_acc.earn_list[0]['ccy'] == 'DOT'
    assert earn_acc.earn_list[1]['ordId'] == '5544530'
    assert earn_acc.earn_list[2]['investData'] == '12.45016778'

# ------------- dicision_making

def test_dicision_making_sell():
    earn_acc = EarnAcc("api_key", "secret_key", "passphrase")
    earn_acc.earn_list = inject_test_data('dicision_earn_list.json')
    earn_acc.account.get_currency = MagicMock()
    earn_acc.account.get_currency.return_value = {'data':[{'bidPx':5}]}

    earn_acc.add_coin.execute = MagicMock()
    earn_acc.add_coin.execute.return_value = None

    earn_acc.list_coin.execute = MagicMock()
    earn_acc.list_coin.execute.return_value = inject_test_data('dicision_list_coin_up.json')

    earn_for_sell = earn_acc.dicision_making()

    assert earn_for_sell[0]['ccy'] == 'DOT'
    