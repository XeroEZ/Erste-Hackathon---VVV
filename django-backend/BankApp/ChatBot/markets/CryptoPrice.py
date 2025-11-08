import requests

def cena_kryptomeny(symbol: str):
    """
    Získa aktuálnu cenu kryptomeny z Binance API.
    :param symbol: napr. 'BTC', 'ETH', 'SOL', 'BNB', 'DOGE'
    """
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}USDT"

    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()

        if "price" in data:
            cena_usd = float(data["price"])
            if cena_usd > 1:
                cena_eur = round(cena_usd * 0.86, 2)
                return f"Aktuálna cena {symbol.upper()} je {cena_usd:.2f} $ alebo {cena_eur:.2f} €."
            else:
                cena_eur = cena_usd * 0.86
                return f"Aktuálna cena {symbol.upper()} je {cena_usd:.9f} $ alebo {cena_eur:.9f} €."
        else:
            return f"Nepodarilo sa nájsť dáta pre {symbol}."

    except requests.exceptions.RequestException as e:
        return f"Chyba pri načítaní dát: {e}"
    except KeyError:
        return "Neočakávaný formát dát z API."
