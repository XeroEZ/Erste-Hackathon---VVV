import requests

API_KEY = "357726899bfc77165d503f6781877f20"
#https://marketstack.com/api-status

def zobraz_cenu(nazov: str, symbol: str):
    """
    Získa aktuálnu cenu akcie/komodity zo služby Marketstack.
    :param nazov: názov spoločnosti alebo komodity (napr. 'Apple')
    :param symbol: burzový symbol (napr. 'AAPL')
    """
    url = f"https://api.marketstack.com/v1/eod/latest?access_key={API_KEY}&symbols={symbol}"

    try:
        resp = requests.get(url)
        resp.raise_for_status()  # kontrola chýb HTTP
        data = resp.json()

        if "data" in data and len(data["data"]) > 0:
            price = data["data"][0]["close"]
            return(f"Aktuálna cena na burze pre {nazov} ({symbol}) je {price}€")
        else:
            return(f"Nepodarilo sa nájsť dáta pre {nazov} ({symbol}).")

    except requests.exceptions.RequestException as e:
        return(f"Chyba pri načítaní dát: {e}")
    except KeyError:
        return("Neočakávaný formát dát z API.")


# 🔹 Príklad použitia:
#print(zobraz_cenu("NVIDIA", "NVDA"))

