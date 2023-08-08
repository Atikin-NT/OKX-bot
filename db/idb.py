from db.database_manager import DataBaseManager

db = DataBaseManager("tests/test.db")

class CreateTable:
    def execute(self):
        db.create_table('funding_acc', {
            'id': 'integer primary key autoincrement',
            'coin_list': 'text not null',
            'coin_usd': 'real not null',
            'time_unix': 'real not null',
        })
        db.create_table('earn_acc', {
            'id': 'integer primary key autoincrement',
            'coin_list': 'text not null',
            'coin_usd': 'real not null',
            'time_unix': 'real not null',
        })
        db.create_table('coin', {
            'id': 'integer primary key autoincrement',
            'ccy': 'real not null',
            'usd': 'real not null',
            'time_unix': 'real not null'
        })


class AddToFundingAcc:
    def execute(self, data: dict) -> bool:
        db.add('funding_acc', data)
        return True
    
class AddToEarnAcc:
    def execute(self, data: dict) -> bool:
        db.add('earn_acc', data)
        return True
    

class AddCoin:
    def execute(self, data: dict) -> bool:
        db.add('coin', data)
        return True


class ListFundingAcc:
    def __init__(self, order_by='time_unix'):
        self.order_by = order_by

    def execute(self, criteria = None, limit = None) -> list:
        return db.select('funding_acc', criteria, self.order_by, limit).fetchall()


class ListEarnAcc:
    def __init__(self, order_by='time_unix'):
        self.order_by = order_by

    def execute(self, criteria = None, limit = None) -> list:
        return db.select('earn_acc', criteria, self.order_by, limit).fetchall()


class ListCoin:
    def __init__(self, order_by='time_unix'):
        self.order_by = order_by

    def execute(self, criteria = None, limit = None) -> list:
        return db.select('coin', criteria, self.order_by, limit).fetchall()
