from logic.base_logic import BaseLogic
from okx.account import Account
from db.idb import AddToFundingAcc
import time
import json

class FundingAcc(BaseLogic):
    def __init__(self, api_key: str, api_secret_key: str, passphrase: str):
        self.account = Account(api_key, api_secret_key, passphrase)
        self.time_unix = time.time()
        self.coin_list = {}
        self.total_usd = 0

    def analize_earn_offers(self) -> str:
        offers = self.account.get_earn_offers()
        offers = list(map(lambda x: { 
                'ccy': x['ccy'],
                'productId': x['productId'],
                'apy': float(x['apy']),
                'term': int(x['term']),
                'state': x['state']
            }, 
            offers['data']))
        offers = [x for x in offers if x['term'] <= 30]
        offers = sorted(offers, key=lambda x: x['apy'], reverse=True)
        return offers[0]['ccy']

    def parse(self) -> None:
        acc_balance = self.account.get_balance()

        coin_amount_list = [coin['availBal'] for coin in acc_balance['data']]
        coin_list = [f'{coin["ccy"]}' for coin in acc_balance['data']]

        assert_valutation = self.account.get_assert_valutation()

        data_to_db = {
            'coin_list': ', '.join(coin_list),
            'coin_usd': assert_valutation['data'][0]['details']['funding'],
            'time_unix': self.time_unix
        }
        
        AddToFundingAcc().execute(data_to_db)

        self.total_usd = float(data_to_db['coin_usd']) 
        self.coin_list = dict(zip(coin_list, coin_amount_list))
    
    def dicision_making(self) -> bool:
        return self.total_usd > 0.001
    
    def dicision_execution(self) -> None:
        for coin, amount in self.coin_list.items():
            if coin == "USDT":
                continue
            estimate = self.account.estimate_convert(coin, amount)
            if estimate['code'] == "52914":
                continue

            quote_id = estimate['data'][0]['quoteId']

            self.account.trade_convert(coin, amount, quote_id)
            time.sleep(1)
        
    