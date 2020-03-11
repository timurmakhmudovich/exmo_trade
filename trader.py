import sys
import requests
import http.client
import urllib
import json
import hashlib
import hmac
import time
import datetime
import pandas as pd

class ExmoAPI:
        def __init__(self, API_KEY, API_SECRET, API_URL = 'api.exmo.me', API_VERSION = 'v1'):
                self.API_URL = API_URL
                self.API_VERSION = API_VERSION
                self.API_KEY = API_KEY
                self.API_SECRET = bytes(API_SECRET, encoding='utf-8')

        def sha512(self, data):
                H = hmac.new(key = self.API_SECRET, digestmod = hashlib.sha512)
                H.update(data.encode('utf-8'))
                return H.hexdigest()

        def api_query(self, api_method, param):
                param =  urllib.parse.urlencode(param)
                sign = self.sha512(param)
                headers = {
                        "Content-type": "application/x-www-form-urlencoded",
                        "Key": self.API_KEY,
                        "Sign": sign
                }
                conn = http.client.HTTPSConnection(self.API_URL)
                conn.request("POST", "/" + self.API_VERSION + "/" + api_method, param, headers)
                response = conn.getresponse().read()
                conn.close()

                try:
                        obj = json.loads(response.decode('utf-8'))
                        """if 'error' in obj and obj['error']:
                                print("URL ACCESS ERROR")
                                raise sys.exit()"""
                        return obj
                except json.decoder.JSONDecodeError:
                        print('Error while parsing response:', response)
                        raise sys.exit()



def healthtest():
        while True:
                params['nonce'] = int(round(time.time() * 1000))
                user_info = ExmoAPI_instance.api_query('user_info', params)
                if 'error' in user_info and user_info['error']:
                        print("URL ACCESS ERROR")
                        time.sleep(5)
                else:
                        break


def order_statistics(params):
        params['nonce'] = int(round(time.time() * 1000))
        order_book = ExmoAPI_instance.api_query('order_book', params)
        required_amount = ExmoAPI_instance.api_query('required_amount', params)
        print(len(order_book[PAIR]['ask']), len(order_book[PAIR]['bid']), required_amount['avg_price'], str(datetime.datetime.now())[11:19])


def check_order_balance(params):
        params['nonce'] = int(round(time.time() * 1000))
        user_info = ExmoAPI_instance.api_query('user_info', params)
        return max(user_info['reserved'][COIN2], user_info['reserved'][COIN1])

def check_crypro_order_balance(params):
        params['nonce'] = int(round(time.time() * 1000))
        user_info = ExmoAPI_instance.api_query('user_info', params)
        return user_info['reserved'][COIN1]

def get_order_id(params):
        params['nonce'] = int(round(time.time() * 1000))
        order_id = ExmoAPI_instance.api_query('user_open_orders', params)[PAIR][0]['order_id']
        return order_id

def check_CRYPT_balance(params):
        params['nonce'] = int(round(time.time() * 1000))
        user_info = ExmoAPI_instance.api_query('user_info', params)
        return user_info['balances'][COIN1]

def check_RUB_balance(params):
        params['nonce'] = int(round(time.time() * 1000))
        user_info = ExmoAPI_instance.api_query('user_info', params)
        return user_info['balances'][COIN2]

def cancel_order(params, order_id):
        params['nonce'] = int(round(time.time() * 1000))
        params['order_id'] = order_id
        ExmoAPI_instance.api_query('order_cancel', params)

def sell_coin(params):
        params['nonce'] = int(round(time.time() * 1000))
        order_buy = ExmoAPI_instance.api_query('order_create', params)


def buy_coin(params):
        params['nonce'] = int(round(time.time() * 1000))
        ExmoAPI_instance.api_query('order_create', params)


def trade():
        a = 0
        while True:
                healthtest()
                crypto_balance = check_CRYPT_balance(params)
                rub_balance = check_RUB_balance(params)
                order_crypto_balance = check_crypro_order_balance(params)
                if check_order_balance(params) != "0":
                        print("Ордер ещё висит. Ждём.")
                        time.sleep(10)
                        if a == 1800 and order_crypto_balance == "0":
                                print("Oтменяем ордер")
                                cancel_order(params, get_order_id(params))
                        a = a + 5
                        print(a)
                else:
                        if crypto_balance != "0":
                                print("Продаем крипту")
                                params['type'] = "sell"
                                params['price'] = sell_price
                                params['quantity'] = crypto_balance
                                buy_coin(params)
                                a = 0
                                time.sleep(300)
                        else:
                                time.sleep(600)
                                print("Покупаем крипту")
                                params['nonce'] = int(round(time.time() * 1000))
                                order_book = ExmoAPI_instance.api_query('order_book', params)[PAIR]
                                current = order_book['ask'][0][0]
                                navar = float(current)*0.005
                                buy_price = float(current) - navar*1.5
                                sell_price = float(current) - navar/2
                                BET = float(rub_balance)/float(buy_price)
                                print(current)
                                print(buy_price)
                                print(sell_price)
                                params['type'] = "buy"
                                params['price'] = buy_price
                                params['quantity'] = BET
                                buy_coin(params)
                                a = 0


COIN1 = "ZEC"
COIN2 = "RUB"
#BET = 0.1
PAIR = COIN1+"_"+COIN2
params = {'pair': PAIR}
ExmoAPI_instance = ExmoAPI('XXXX', 'XXXX')


trade()


"""
trades = ExmoAPI_instance.api_query('trades', params)
df = pd.DataFrame(trades[PAIR]).sort_values('date')
df_buy = df[df['type'] == 'buy'].sort_values('price').to_dict('r')
df_sell = df[df['type'] == 'sell'].sort_values('price').to_dict('r')


order_book = ExmoAPI_instance.api_query('order_book', params)[PAIR]
current = order_book['ask'][0][0]
buy_price = float(current) - 100
sell_price = float(current)

print(current)
print(buy_price)
print(sell_price)
print(check_order_balance(params))
print(check_CRYPT_balance(params))

params['quantity'] = "0.01"
params['price'] = buy_price
params['type'] = "buy"
params['nonce'] = int(round(time.time() * 1000))
"""
