import requests

API_KEY = "KegZpgZBwQSbSw5sPfLYlzXa6wwM7Oqt"  # môžeš použiť "demo" na test alebo si spraviť vlastný free key
BASE_URL = "https://financialmodelingprep.com/api/v3"

def zobraz_cenu(nazov: str, symbol: str):
    if symbol.lower() in ["gold", "silver", "oil", "crude", "brent"]:
        url = f"{BASE_URL}/quotes/commodity?apikey={API_KEY}"
    else:
        url = f"{BASE_URL}/quote/{symbol}?apikey={API_KEY}"

    resp = requests.get(url)
    data = resp.json()

    # ak sú to komodity
    if isinstance(data, list) and len(data) > 0:
        for item in data:
            if nazov.lower() in item["name"].lower():
                price = item.get("price")
                return f"Aktuálna cena {item['name']} je {price} USD"
        return f"Nepodarilo sa nájsť cenu pre {nazov}"
    # ak sú to akcie
    elif isinstance(data, list) and len(data) == 1:
        price = data[0].get("price")
        return f"Aktuálna cena na burze pre {nazov} ({symbol}) je {price} USD"
    else:
        return f"Nepodarilo sa načítať dáta. Odpoveď: {data}"

# 🔹 Príklady:
print(zobraz_cenu("Apple", "AAPL"))
print(zobraz_cenu("NVIDIA", "NVDA"))
print(zobraz_cenu("Zlato", "gold"))
print(zobraz_cenu("Ropa", "crude oil"))
