#from binance.client import Client
import unicodedata
import json
import requests
import datetime
import numpy as np
import matplotlib.pyplot as plt
# Definir a URL da API do CoinGecko para obter o preço do BTC em uma data específica
# https://www.coingecko.com/pt/api/documentation
base_url = 'http://api.coingecko.com/api/v3/coins'


def verify_exists_coin(coin):
    #Verificar nas já existentes
    print("Consultando JSON...")
    
    
    #print("Chamando API...")
    url = f'{base_url}/list'
    response = requests.get(url)
    if response.status_code == 200:
        with open('coins.json', 'w', encoding='utf-8') as jp:
            js = json.dumps(response.json(), indent=4)
            jp.write(js)
        for coin_index in response.json():
            if coin_index['symbol'] == coin:
                return coin_index
    return {'id': 'none', 'symbol': 'none', 'name': 'none'}
print(verify_exists_coin('eth'))

def get_price_coin(coin, data):
    json_coin = verify_exists_coin(coin)
    print("Verificar se a moeda existe") if json_coin == {'id': 'none', 'symbol': 'none', 'name': 'none'} else ''
    # Ex. Coin: bitcoin, ethereum,
    url = f'{base_url}/{json_coin["id"]}/history'
    params = {
        'date': data
    }

    # Fazer a solicitação GET para a API do CoinGecko
    response = requests.get(url, params=params)
    # Verificar o código de status da resposta
    if response.status_code == 200:
        # A resposta foi bem-sucedida, obter o preço do BTC na data específica valor.replace(" / ", "_").replace(" - ", "").replace(" ", "_").replace("/", "").upper()
        body = response.json()['market_data']
        logo = response.json()['image']['small']
        btc_price = round(body['current_price']['usd'], 2)
        print(f'O preço do {json_coin["name"]} em {data} foi: ${btc_price}')
    else:
        print('Não foi possível obter o preço do Bitcoin na data específica.', response)


#print(get_price_coin('eth', '10-10-2022'))


def get_price_coin_range(coin, timestamp_start, timestamp_end):
    json_coin = verify_exists_coin(coin)
    if json_coin == 429:
        return "429"    
    url = f'{base_url}/bitcoin/market_chart/range?=&from={timestamp_start}&to={timestamp_end}&vs_currency=usd'
    list_prices = []
    # Fazer a solicitação GET para a API do CoinGecko
    print(url)
    response = requests.get(url)
    # Verificar o código de status da resposta
    if response.status_code == 200:
      # A resposta foi bem-sucedida, obter o preço do BTC na data específica valor.replace(" / ", "_").replace(" - ", "").replace(" ", "_").replace("/", "").upper()
      #print(response.json()['prices'])
      for resp in response.json()['prices']:

          # Obter a data e hora atuais
          data = datetime.datetime.fromtimestamp(int(str(resp[0])[:10]))
          list_prices.append(round(resp[1], 2))
          #print("Data:", str(data)[:10], "Valor:", round(resp[1], 2))
        #body = response.json()['market_data']
        #logo = response.json()['image']['small']
        #btc_price = round(body['current_price']['usd'], 2)
        #print(f'O preço do {json_coin["name"]} em {data} foi: ${btc_price}')
    else:
        print('Não foi possível obter o preço do Bitcoin na data específica.', response)
    return list_prices
    plt.plot(list_prices)

print(get_price_coin_range('btc', int(datetime.datetime(2021, 1, 1).timestamp()), int(datetime.datetime(2023, 1, 1).timestamp()))) # Ano, mês, dia

# Definir a data a ser convertida em timestamp
timestamp_segundos = int(datetime.datetime(2011, 6, 1).timestamp())  # Ano, mês, dia

#print("Timestamp em segundos:", timestamp_segundos)

resposta = {
  "prices": [
    [
      1577923200000,
      7193.7546679601
    ],
    [
      1578009600000,
      6963.853353983485
    ],
    [
      1578096000000,
      7300.34693530511
    ]
  ]
}
