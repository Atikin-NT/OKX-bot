from .client import Client
from . import consts as c

class Account(Client):

    def __init__(self, api_key: str, api_secret_key: str, passphrase: str):
        super().__init__(api_key, api_secret_key, passphrase)

    def _partition(self, l, n) -> list:
        for i in range(0, len(l), n):
            yield l[i:i+n]
    
    def get_balance(self) -> any:
        return super().request_without_params(c.GET, c.GET_BALANCES)
    
    def get_earn_active(self) -> any:
        return super().request_without_params(c.GET, c.STACK_DEFI_ORDERS_ACTIVITY)
    
    def get_earn_offers(self, protocol_type='staking') -> any:
        params = {
            'protocolType': protocol_type
        }
        return super().request_with_params(c.GET, c.STACK_DEFI_OFFERS, params)
    
    def get_currency(self, inst_id) -> any:
        return super().request_with_params(c.GET, c.TICKER_INFO, inst_id)

    def get_assert_valutation(self) -> any:
        return super().request_with_params(c.GET, c.ASSET_VALUATION, {'ccy': 'USDT'})
    
    def estimate_convert(self, from_ccy, amount, to_ccy="USDT", side="sell", rfqSzCcy=None) -> any:
        params = {
            "baseCcy": from_ccy,
            "quoteCcy": to_ccy,
            "side": side,
            "rfqSz": amount,
            "rfqSzCcy": rfqSzCcy or from_ccy
        }
        return super().request_with_params(c.POST, c.ESTIMATE_QUOTE, params)
    
    def trade_convert(self, from_ccy: str, amount: str, quote_id: str, to_ccy="USDT", side='sell', szCcy=None) -> any:
        params = {
            "baseCcy": from_ccy,
            "quoteCcy": to_ccy,
            "side": side,
            "sz": amount,
            "szCcy": szCcy or from_ccy,
            "quoteId": quote_id
        }
        return super().request_with_params(c.POST, c.CONVERT_TRADE, params)

    def purchase_earn(self, product_id: str, ccy: str, amount: str, term: str) -> any:
        params = {
            "productId": product_id,
            "investData": {
                "ccy": ccy,
                "amt": amount
            },
            "term": term
        }
        return super().request_with_params(c.POST, c.STACK_DEFI_PURCHASE)

    def cancel_earn(self, ord_id: str, protocol_type: str) -> any:
        params = {
            'ordId': ord_id,
            'protocolType': protocol_type
        }
        return super().request_with_params(c.POST, c.STACK_DEFI_CANCEL, params)
