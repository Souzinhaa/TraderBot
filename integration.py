# Usar python 3.9 e TA_Lib-0.4.24-cp39-cp39-win_amd64.whl
# from binance.client import Clientcommand:workbench.trust.manage
import unicodedata
import json
import requests
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import plotly.graph_objects as go
import pandas_datareader as pdr
import pandas as pd
import yfinance as yf
import statsmodels.api as sm
from collections import defaultdict
import prices as pc
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import utils

matplotlib.style.use('ggplot')
# Definir a URL da API do CoinGecko para obter o preço do BTC em uma data específica
# https://www.coingecko.com/pt/api/documentation
base_url = 'http://api.coingecko.com/api/v3/coins'
path = utils.path

def verify_exists_coin(coin):
    # Verificar nas já existentes
    file_coins = open(path + 'coins.json')
    coins_json = json.load(file_coins)
    for coin_index in coins_json:
        if coin_index['symbol'] == coin:
            return coin_index
    # Confirmar na API
    print("Chamando API...")
    url = f'{base_url}/list'
    response = requests.get(url)
    if response.status_code == 200:
        with open(path + 'coins.json', 'w', encoding='utf-8') as jp:
            js = json.dumps(response.json(), indent=4)
            jp.write(js)
        for coin_index in response.json():
            if coin_index['symbol'] == coin:
                return coin_index
    return {'id': 'none', 'symbol': 'none', 'name': 'none'}
# print(verify_exists_coin('eth'))

def get_price_coin_range(coin, timestamp_start, timestamp_end):
    json_coin = verify_exists_coin(coin)
    if json_coin == {'id': 'none', 'symbol': 'none', 'name': 'none'}:
        return "Verificar se a moeda existe"
    url = f'{base_url}/{json_coin["id"]}/market_chart/range?=&from={timestamp_start}&to={timestamp_end}&vs_currency=usd'

    list_prices = {'date':[],
                   'close':[]
                   }
    # Fazer a solicitação GET para a API do CoinGecko
    response = requests.get(url)
    #print(url)
    # Verificar o código de status da resposta
    if response.status_code == 200:         
        with open(path + 'mockBtc.json', 'w') as arquivo_json:
            json.dump(response.json()['prices'], arquivo_json)       
    
        for resp in response.json()['prices']:
            list_prices['date'].append(utils.convert_timestamp_to_datetime(resp[0]))
            list_prices['close'].append(round(resp[1], 2))
        list_prices_df = pd.DataFrame(list_prices)
        #list_prices.rename({0: "date", 1: "close"}, axis=1, inplace=True)
    else:
        print(
            f'Não foi possível obter o preço do {json_coin["id"]} na data específica.', response)
        mock = json.load(open('mockBtc.json'))
        for resp in mock:
            list_prices['date'].append(utils.convert_timestamp_to_datetime(resp[0]))
            list_prices['close'].append(round(resp[1], 2))
        list_prices_df = pd.DataFrame(list_prices)
    list_prices_df = list_prices_df.set_index('date')
    return list_prices_df

#print(get_price_coin_range('btc', int(datetime.datetime(2011, 1, 1).timestamp()), int(datetime.datetime(2023, 9, 28).timestamp()))) # Ano, mês, dia

# Definir a data a ser convertida em timestamp
timestamp_segundos = int(datetime.datetime(2011, 6, 1).timestamp())  # Ano, mês, dia

#print("Timestamp em segundos:", timestamp_segundos)


def get_price_coin_ohlc(coin):
    json_coin = verify_exists_coin(coin)
    if json_coin == {'id': 'none', 'symbol': 'none', 'name': 'none'}:
        return "Verificar se a moeda existe"
    url = f'{base_url}/{json_coin["id"]}/ohlc?vs_currency=usd&days=max&precision=2'
    # Fazer a solicitação GET para a API do CoinGecko
    response = requests.get(url)
    ohlc = []
    # Verificar o código de status da resposta
    if response.status_code == 200:
        with open(path + 'mockBtcOhlc.json', 'w') as arquivo_json:
            json.dump(response.json(), arquivo_json)
        for resp in response.json():
            list_ohlc = []
            # Obter a data e hora atuais
            list_ohlc.append(utils.convert_timestamp_to_datetime(resp[0]))
            list_ohlc.append(resp[1])
            list_ohlc.append(resp[2])
            list_ohlc.append(resp[3])
            list_ohlc.append(resp[4])
            ohlc.append(list_ohlc)
        
        ohlc_final = pd.DataFrame(ohlc)
        ohlc_final.rename({0: "date", 1: "open", 2: "high", 3: "low", 4: "close"}, axis=1, inplace=True)
        ohlc_final.index = ohlc_final['date']
        return ohlc_final #time, open, high, low, close
    else:
        print(f'Não foi possível obter o preço do {json_coin["id"]} na data específica.', response)
        mock = json.load(open('mockBtcOhlc.json'))
        for resp in mock:
            list_ohlc = []
            # Obter a data e hora atuais
            list_ohlc.append(utils.convert_timestamp_to_datetime(resp[0]))
            list_ohlc.append(resp[1])
            list_ohlc.append(resp[2])
            list_ohlc.append(resp[3])
            list_ohlc.append(resp[4])
            ohlc.append(list_ohlc)
        ohlc_final = pd.DataFrame(ohlc)
        ohlc_final.rename({0: "date", 1: "open", 2: "high", 3: "low", 4: "close"}, axis=1, inplace=True)
        ohlc_final = ohlc_final.set_index('date')
        return ohlc_final #time, open, high, low, close

#print(get_price_coin_ohlc('btc'))
#print(get_price_coin_ohlc('eth'))