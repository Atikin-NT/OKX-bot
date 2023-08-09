from logic.base_logic import BaseLogic
from okx.account import Account
from db.idb import AddCoin, ListCoin
import json
import time

class EarnAcc(BaseLogic):
    """
    Отвечает за проверку текущих вложений и если крипта упала, то
    выводим из вложения. 
    """
    def __init__(self, api_key: str, api_secret_key: str, passphrase: str):
        self.account = Account(api_key, api_secret_key, passphrase)
        self.time_unix = time.time()
        self.earn_list = []
        self.total_usd = 0
        self.add_coin = AddCoin()
        self.list_coin = ListCoin(order_by="time_unix desc")

    def parse(self) -> None:
        resp_earn_active = self.account.get_earn_active()
        earn_for_analize = []
        for earn in resp_earn_active['data']:
            if earn['term'] != 0:
                earn_for_analize.append({
                    'ordId': earn['ordId'],
                    'ccy': earn['ccy'],
                    'investData': earn['investData'][0]['amt'],
                    'earningData': earn['earningData'][0]['earnings']
                })
        self.earn_list = earn_for_analize

    def _dicision_on_coin_history(self, ccy: str) -> bool:
        coin_history = self.list_coin.execute({'ccy': ccy}, 10)
        coin_per_result = float(coin_history[0]['usd'] / coin_history[-1]['usd'])
        
        if coin_history[0]['usd'] < coin_history[-1]['usd'] and coin_per_result < 0.9:
            return True
        return False
    
    def dicision_making(self) -> list:
        earn_for_sell = []
        for coin in self.earn_list:
            ticker = self.account.get_currency({'instId': f'{coin["ccy"]}-USDT'})
            self.add_coin.execute({
                'ccy': coin['ccy'],
                'usd': ticker['data'][0]['bidPx'],
                'time_unix': self.time_unix
            })

            if self._dicision_on_coin_history(coin['ccy']):
                earn_for_sell.append(coin)
        
        return earn_for_sell
    
    def dicision_execution(self, earn_for_sell: list) -> None:
        for coin in earn_for_sell:
            self.account.redeem_earn(
                ord_id=coin['ordId'],
                protocol_type='staking'
            )
            time.sleep(0.5)
