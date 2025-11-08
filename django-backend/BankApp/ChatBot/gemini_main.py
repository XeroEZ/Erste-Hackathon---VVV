from . import geminiKey
from . import AI_databaza
from .markets import StockPrice
from .markets import ComodityPrice
from .markets import CryptoPrice


def OtazkaNaGeminiBasic(prompt_text) -> str:

    try:
        client = geminiKey.ClientApi()

        config = geminiKey.types.GenerateContentConfig(
            temperature=0.0
        )


        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text,
            config=config,
        )
        return response.text.strip()

    except Exception as e:
        return f"Nastala chyba pri volaní AI: {e}"


def OtazkaUzivatela(OtazkaUzivatela):

    prompt_text_for_split = (
        "Si klasifikačný nástroj. Tvojou jedinou úlohou je určiť, do ktorej z kategórií patrí nasledujúca otázka."
        "\n1. **Stocko (Akcie/Cenné papiere):** otázky o cenách akcií, indexov, ETF, dlhopisov."
        "\n2. **Komodity:** otázky o investičných a obchodovaných fyzických komoditách (napr. zlato, striebro, ropa, pšenica, káva). *NEZAHŔŇA nákupy bežného spotrebného tovaru.*"
        "\n3. **Krypto:** otázky o kryptomenách (Bitcoin, Ethereum, Solana, Dogecoin...)."
        "\n4. **Iné:** Všetko ostatné, vrátane otázok o **osobných nákupoch** bežného spotrebného tovaru (ako **mäso, oblečenie**, potraviny, elektronika, atď.) a otázok nesúvisiacich s investíciami."
        "\n**Odpoveď musí byť len jedno slovo: 'Stocko', 'Komodity', 'Krypto' alebo 'Iné'.**"
        f"\nOtázka: \"{OtazkaUzivatela}\""
    )
    split = OtazkaNaGeminiBasic(prompt_text_for_split)

    if "Stock" in split:
        print("Stock")
        return Stock(OtazkaUzivatela)
    elif "Komodity" in split:
        print("Komodity")
        return Comodity(OtazkaUzivatela)
    elif "Krypto" in split:
        print("Krypto")
        return Crypto(OtazkaUzivatela)
    else:
        print("Ine")
        return AI_databaza.AI(OtazkaUzivatela)

def Stock(OtazkaUzivatela):
    prompt_text_for_split = (f"Rozdel otazku uzivatela na Nazov stock a medzinarodnu skratku stock. A odpis mi 'Nazov,Skratku'. \nOtazka uzivatela: {OtazkaUzivatela}"
        )
    resp = OtazkaNaGeminiBasic(prompt_text_for_split)
    print(resp)
    Nazov, symbol = resp.split(",")


    return StockPrice.zobraz_cenu(Nazov,symbol)

def Comodity(OtazkaUzivatela):
    prompt_text_for_split = (
        "Rozdel otázku používateľa na názov komodity a jej API názov podľa služieb API Ninjas "
        "(napr. 'platinum', 'micro_silver', 'oat', 'micro_gold', 'feeder_cattle', 'rough_rice', 'class_3_milk'). "
        "Odpíš mi vo formáte 'Nazov,API_nazov'. Ak komodita nie je medzi dostupnými, odpíš presne 'neznamy'.\n"
        f"Otázka používateľa: {OtazkaUzivatela}"
    )

    resp = OtazkaNaGeminiBasic(prompt_text_for_split).strip()

    if "neznamy" in resp.lower():
        return "K tejto komodite nemám prístup. Pretoze studenti ktori vyvijali tento system nemaju peniaze na drahe API."

    try:
        nazov, api_nazov = [s.strip() for s in resp.split(",")]
        return ComodityPrice.cena_komodity(api_nazov)
    except Exception as e:
        return f"Nepodarilo sa spracovať odpoveď AI: {resp} ({e})"

def Crypto(OtazkaUzivatela):
    prompt_text_for_split = (
        "Rozdel otázku používateľa na názov kryptomeny a jej symbol používaný na Binance (napr. BTC, ETH, SOL, BNB, DOGE). "
        "Odpíš vo formáte 'Nazov,Symbol'. Ak kryptomena nie je podporovaná, odpíš presne 'neznamy'.\n"
        f"Otázka používateľa: {OtazkaUzivatela}"
    )

    resp = OtazkaNaGeminiBasic(prompt_text_for_split).strip()

    if "neznamy" in resp.lower():
        return "K tejto kryptomene nemám prístup."

    try:
        nazov, symbol = [s.strip() for s in resp.split(",")]
        return CryptoPrice.cena_kryptomeny(symbol)
    except Exception as e:
        return f"Nepodarilo sa spracovať odpoveď AI: {resp} ({e})"


def main():
    print("Vitaj v komunikacije s Gemini")
    # spýtaj sa používateľa na odpoveď

    user_input = input("Zadaj svoju otazku? ")


    # volanie tvojej funkcie AkinatorHra s parametrom
    result = OtazkaUzivatela(user_input)
    # vypíš výsledok
    print(f"\033[92mVýsledok: {result}\033[0m")



if __name__ == "__main__":
    main()

