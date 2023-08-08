import pytest
import time
from db.idb import CreateTable, AddCoin, AddStatistic, ListCoin, ListStatistic


CreateTable().execute()

t = time.time()

def test_add_coin():
    data = {
        'coin': 'USDT',
        'coin_count': 930359.9998,
        'coin_usd': 930359.9998,
        'time_unix': t,
    }
    AddCoin().execute(data)

    data = {
        'coin': 'BTC',
        'coin_count': 33.6799714158199414,
        'coin_usd': 1239950.9687532129092577,
        'time_unix': t,
    }
    AddCoin().execute(data)

def test_add_statistic():
    data = {
        'total_usd': 10679688.0460531643092577,
        'time_unix': t,
    }
    AddStatistic().execute(data)

def test_list_coin():
    coin_list = ListCoin().execute()
    assert coin_list[0]['coin_count'] == 930359.9998
    assert coin_list[0]['coin_usd'] == 930359.9998
    assert coin_list[0]['time_unix'] == t

    assert coin_list[1]['coin_count'] == 33.6799714158199414
    assert coin_list[1]['coin_usd'] == 1239950.9687532129092577
    assert coin_list[1]['time_unix'] == t

def test_list_statistic():
    stat_list = ListStatistic().execute()
    assert stat_list[0]['total_usd'] == 10679688.0460531643092577
    assert stat_list[0]['time_unix'] == t
