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

matplotlib.style.use('ggplot')
# Definir a URL da API do CoinGecko para obter o preço do BTC em uma data específica
# https://www.coingecko.com/pt/api/documentation
base_url = 'http://api.coingecko.com/api/v3/coins'
