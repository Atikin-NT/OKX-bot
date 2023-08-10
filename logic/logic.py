from logic.funding_acc import FundingAcc
from logic.earn_acc import EarnAcc

class Logic:
    def __init__(self, api_key: str, api_secret_key: str, passphrase: str):
        self.funding_acc = FundingAcc(api_key, api_secret_key, passphrase)
        self.earn_acc = EarnAcc(api_key, api_secret_key, passphrase)

    def funding_account(self):
        self.funding_acc.analize_earn_offers()

        self.funding_acc.parse()

        if self.funding_acc.dicision_making():
            self.funding_acc.dicision_execution()

        self.funding_acc.choose_earn()

    def earn_account(self):
        self.earn_acc.parse()

        earn_for_sell = self.earn_acc.dicision_making()
        if earn_for_sell != []:
            self.earn_acc.dicision_execution(earn_for_sell)
