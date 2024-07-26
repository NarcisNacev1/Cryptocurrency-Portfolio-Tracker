import requests
from Backend.src.constants import API_URL
from decimal import Decimal


def get_crypto_prices(crypto):
    url = f"{API_URL}?ids={crypto}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return Decimal(str(data[crypto]["usd"]))


def get_cryptos(cryptocurrencies):
    ids = ','.join(cryptocurrencies)
    url = f"{API_URL}?ids={ids}&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        prices = {crypto: Decimal(str(data[crypto]['usd'])) for crypto in cryptocurrencies if crypto in data    }
        return prices
    else:
        raise ConnectionError(f'Failed to collect data from CoinGeckoAPI: {response.status_code}')
