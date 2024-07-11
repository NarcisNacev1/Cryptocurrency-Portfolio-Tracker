import requests
from Backend.src.constants import API_URL
from decimal import Decimal


def get_crypto_prices(crypto):
    url = f"{API_URL}?ids={crypto}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return Decimal(str(data[crypto]["usd"]))