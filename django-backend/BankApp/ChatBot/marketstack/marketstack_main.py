import requests

API_KEY = "357726899bfc77165d503f6781877f20"
symbol = "NVDA"
url = f"https://api.marketstack.com/v1/eod/latest?access_key={API_KEY}&symbols={symbol}"

resp = requests.get(url)
data = resp.json()
price = data["data"][0]["close"]
print(f"Aktuálna cena {symbol}: {price} USD")
