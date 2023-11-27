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

def calcular_informacoes_operacao(coin, date, amount, price, operation, number):
    # Carrega a carteira existente
    carteira = utils.ler_carteira_json(number)
    trade = True
    # Crie um dicionário para representar a operação
    operacao = {
        "date": date,
        "amount": amount,
        "price": price,
        "operation": operation,
        "value_operation": str(float(amount) * float(price))
    }
    if coin not in carteira:
        carteira[coin] = [{
        "date": date,
        "amount": '0',
        "price": '0',
        "operation": 'inicialize',
        "value_operation": '0',
        "wallet_usd": '0',
        "price_middle": '0',
        "amount_total": '0'
    }]
        
    for op in carteira[coin]:
        if date in op['date'] and op['operation'] != 'inicialize':
            trade = False
            
    if ((float(carteira[coin][-1]["amount_total"]) >= float(operacao['amount'])) or operation == 'buy') and trade:
        if (coin in carteira):
            if operation == "buy":
                # Cálculos para operações de compra
                operacao["wallet_usd"] = str(float(carteira[coin][-1]["wallet_usd"]) - float(operacao["value_operation"]))
                operacao["amount_total"] = str(float(carteira[coin][-1]["amount_total"]) + float(amount))
                operacao["price_middle"] = str(round((float(carteira[coin][-1]["price_middle"]) * float(carteira[coin][-1]["amount_total"]) +
                    float(operacao["value_operation"])) / (float(carteira[coin][-1]["amount_total"]) + float(amount)), 2))
                operacao["earnings"] = str(round(((float(operacao["price_middle"]) / float(price) - 1) * 100), 2))
                #print("Compra realizada ", date, '\n')
            elif operation == "sell":
                # Cálculos para operações de venda
                operacao["wallet_usd"] = str(float(carteira[coin][-1]["wallet_usd"]) + float(operacao["value_operation"]))
                operacao["amount_total"] = str(float(carteira[coin][-1]["amount_total"]) - float(amount))
                operacao["price_middle"] = str(round(float(carteira[coin][-1]["price_middle"]), 2))
                operacao["earnings"] = str(round(((float(operacao["value_operation"]) / (float(carteira[coin][-1]["price_middle"]) * float(amount)) - 1) * 100), 2))
                #print("Venda realizada ", date, '\n')
            operacao["earnings"] = operacao["earnings"] + "%"


        else:
            operacao["wallet_usd"] =  "-" + operacao["value_operation"]
            operacao["amount_total"] =  amount
            operacao["price_middle"] =  price
            operacao["earnings"] =  "0%"
            carteira[coin] = []
        # Adicione a operação à lista de investimentos na carteira
        carteira[coin].append(operacao)
    else:
        #print("Venda não pode ser realizada por falta de saldo", date, '\n')
        return {}
    
    
    return utils.gravar_carteira_json(carteira, number)

# Exemplo de uso:
#novo_carteira_json = calcular_informacoes_operacao("BTC", "2018-07-28", "0.01", "5853", "buy")
#novo_carteira_json = calcular_informacoes_operacao("BTC", "2023-11-11", "0.0059", "36642", "buy")
#novo_carteira_json = calcular_informacoes_operacao("BTC", "2023-11-11", "0.0022", "37196", "sell")
#novo_carteira_json = calcular_informacoes_operacao("BTC", "2014-11-13", "0.0022", "36700", "buy", 'aaax')
#print(json.dumps(novo_carteira_json, indent=4))