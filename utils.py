# Usar python 3.9 e TA_Lib-0.4.24-cp39-cp39-win_amd64.whl
# from binance.client import Clientcommand:workbench.trust.manage
import unicodedata
import json
import requests
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import talib
import plotly.graph_objects as go
import pandas_datareader as pdr
import pandas as pd
import yfinance as yf
import statsmodels.api as sm
import pandas_ta as pdta
from collections import defaultdict
import prices as pc
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


matplotlib.style.use('ggplot')
# Definir a URL da API do CoinGecko para obter o preço do BTC em uma data específica
# https://www.coingecko.com/pt/api/documentation
base_url = 'http://api.coingecko.com/api/v3/coins'

arquivo_json = "transactions.json"
path = 'C:/Users/Adrian/Dropbox/Projeto TCC Trade/transacoes/'
def convert_timestamp_to_datetime(timestamp):
    data = datetime.datetime.fromtimestamp(timestamp/1000)
    data = data.strftime("%Y-%m-%d 00:00:00")
    return pd.Timestamp(data)

#print(type(convert_timestamp_to_datetime(1578009600000)), convert_timestamp_to_datetime(1578009600000))

def slice_per_month(df, months, corte):
    last_index = df.index[-1]
    last_register = last_index - pd.DateOffset(months=months)
    if corte == 0:
        df = df.loc[last_register:]
    elif corte < 0:
        df = df.loc[last_register:][corte:]
    else:
        df = df.loc[last_register:][:corte]
    return df


def convert_ohlc(df_crypto):
    # Bollinger Bands 
    df_crypto['sma'] = talib.SMA(df_crypto['close'], 7) # Padrão 30 períodos
    upper, middle, lower = (nullos.dropna() for nullos in talib.BBANDS(df_crypto['close'], matype= talib.MA_Type.T3))
    
    det = pd.concat([upper,lower,df_crypto['close']],axis=1,join="inner")
    return det


def ler_carteira_json(number):
    try:
        with open(path + str(number) + arquivo_json, "r") as file:
            carteira = json.load(file)
        return carteira
    except FileNotFoundError:
        return {}
    
def gravar_carteira_json(carteira, number):        
    try:
        # Salve a carteira atualizada no arquivo JSON
        caminho = str(number) + arquivo_json
        with open(path + caminho, "w") as file:
            json.dump(carteira, file, indent=4)
        return carteira
    except FileNotFoundError:
        return {}
    
def gravar_resultados_json(resultados):        
    try:
        lista = []
        # Salve a carteira atualizada no arquivo JSON
        with open(path + 'results.json', "r") as file:
            lista = json.load(file)
        lista = lista + resultados
        with open(path + 'results.json', "w") as file:
            json.dump(lista, file, indent=4)
        return lista
    except FileNotFoundError:
        return {}