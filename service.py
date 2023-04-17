import requests
from bs4 import BeautifulSoup


def getCriptoCurrentValue():
    # URL da página a ser solicitada
    url = "https://coinmarketcap.com/pt-br/"

    # Fazer a solicitação GET da página e armazenar o conteúdo em uma variável
    response = requests.get(url)
    content = response.content

    # Criar o objeto BeautifulSoup a partir do conteúdo HTML
    soup = BeautifulSoup(content, "html.parser")

    # Procurar as tags de preço para Bitcoin e Ethereum
    bitcoin_price = soup.find("a", {"href": "/pt-br/currencies/bitcoin/markets/"}).text
    ethereum_price = soup.find("a", {"href": "/pt-br/currencies/ethereum/markets/"}).text

    # Imprimir os preços encontrados
    print("Preço do Bitcoin (BTC): " + bitcoin_price)
    print("Preço do Ethereum (ETH): " + ethereum_price)
