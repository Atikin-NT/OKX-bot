from logic.base_logic import BaseLogic
from okx.account import Account
from db.idb import AddToFundingAcc
import time
import json

class FundingAcc(BaseLogic):
    """
    Переводит поступившие активы в USDT
    Если накопилось достаточно USDT, то ищет самое выгодное предложение
    по вложениям и вкладывает в него
    """
    def __init__(self, api_key: str, api_secret_key: str, passphrase: str):
        self.account = Account(api_key, api_secret_key, passphrase)
        self.time_unix = time.time()
        self.coin_list = {}
        self.total_usd = 0

    def parse(self) -> None:
        """
        Получаем текущий баланс на аккаунте
        """
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
        """
        Функция принятия решения о переводе в USDT
        """
        return self.total_usd > 0.001
    
    def dicision_execution(self) -> None:
        """
        Операция перевода в USDT
        """
        for coin, amount in self.coin_list.items():
            if coin == "USDT":
                continue
            estimate = self.account.estimate_convert(coin, amount)
            if estimate['code'] == "52914":
                continue

            time.sleep(1)

            quote_id = estimate['data'][0]['quoteId']

            convert_resp = self.account.trade_convert(coin, amount, quote_id)
            print(convert_resp)
            if convert_resp['data'][0]['state'] != 'fullyFilled':
                print('error')
            time.sleep(1)
        

    def analize_earn_offers(self) -> list:
        """
        Поиск 10 самых выгодных предложений
        """
        offers = self.account.get_earn_offers()
        time.sleep(1)
        offers = list(map(lambda x: { 
                'ccy': x['ccy'],
                'productId': x['productId'],
                'apy': float(x['apy']),
                'term': int(x['term']),
                'state': x['state'],
                'minAmt': x['investData'][0]['minAmt'],
                'maxAmt': x['investData'][0]['maxAmt']
            }, 
            offers['data']))
        offers = [x for x in offers 
                  if x['term'] < 30 and 
                     x['state'] == 'purchasable']
        offers = sorted(offers, key=lambda x: x['apy'], reverse=True)
        return offers[:10]
    
    def _get_usd_balance(self) -> int:
        balance = self.account.get_balance()
        for coin in balance['data']:
            if coin['ccy'] == 'USDT':
                return coin['availBal']
        return 0
    
    def choose_earn(self):
        """
        Операция покупки оффера
        """
        self.total_usd = self._get_usd_balance()
        print(self.total_usd)
        offers = self.analize_earn_offers()

        for offer in offers:
            print(offer['ccy'])
            estimate = self.account.estimate_convert(
                from_ccy=offer['ccy'], 
                amount=self.total_usd,
                rfqSzCcy='USDT',
                side='buy')
            print(estimate)
            time.sleep(1)
            
            if estimate['code'] != "0" or float(estimate['data'][0]['baseSz']) <= float(offer['minAmt']):
                print('so small :(')
                continue

            quote_id = estimate['data'][0]['quoteId']

            convert_resp = self.account.trade_convert(
                from_ccy=offer['ccy'], 
                amount=self.total_usd, 
                quote_id=quote_id,
                szCcy='USDT',
                side='buy')
            time.sleep(1)
            print(convert_resp)
            if convert_resp['data'][0]['state'] != 'fullyFilled':
                print('error')
                continue

            earn_resp = self.account.purchase_earn(
                offer['productId'],
                offer['ccy'],
                convert_resp['data'][0]['fillBaseSz'],
                offer['term'])
            if earn_resp['code'] == 0:
                return
            time.sleep(1)
        
    