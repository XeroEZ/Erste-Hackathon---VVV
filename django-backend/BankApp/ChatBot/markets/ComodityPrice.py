import requests

API_KEY = "K4pIQ52ezMCsHV5+BYAPhQ==xG6i2YH04jSVr8UH"

def cena_komodity(komodita: str):
    """
    Získa aktuálnu cenu komodity z API Ninjas.
    :param komodita: názov komodity v angličtine, napr. 'platinum', 'gold', 'crude_oil'
    """
    url = f"https://api.api-ninjas.com/v1/commodityprice?name={komodita}"
    headers = {"X-Api-Key": API_KEY}

    try:
        resp = requests.get(url, headers=headers)
        
        resp.raise_for_status()
        data = resp.json()
        return f"Aktualna cena {komodita} je: {round(data["price"] * 0.86, 2)} €."

    except requests.exceptions.RequestException as e:
        return f"Chyba pri načítaní dát: {e}"
    except (KeyError, IndexError):
        return "Neočakávaný formát dát z API."


# 🔹 Príklad použitia:
print(cena_komodity("platinum"))
