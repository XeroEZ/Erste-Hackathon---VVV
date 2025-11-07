from . import geminiKey
from .markets import StockPrice

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

    prompt_text_for_split = ("Si klasifikačný nástroj. Tvojou jedinou úlohou je určiť, do ktorej z troch kategórií patrí nasledujúca otázka od používateľa."
    "\n1. **Stocko (Akcie/Cenné papiere):** Otázka sa týka ceny akcií konkrétnej spoločnosti (napr. Tesla, Apple, Kofola, Microsoft, ČEZ), indexov (S&P 500, NASDAQ, DAX), burzových fondov (ETF), dlhopisov, alebo iných cenných papierov kótovaných na burze."
    "\n2. **Komodity:** Otázka sa týka ceny alebo informácií o fyzických surovinách a komoditách (napr. Zlato, Striebro, Ropa, Zemný plyn, Pšenica, Káva, Meď, Drevo, Uhlie)."
    "\n3. **Iné:** Otázka nespadá pod kategóriu Stocko ani Komodity (napr. Kryptomeny, Makroekonomické dáta, História, Počasie, Šport, atď.)."
    "\n**Tvoja odpoveď MUSÍ byť len jedno slovo z nasledovného zoznamu: 'Stocko', 'Komodity' alebo 'Iné'.** Žiadny iný text, vysvetlenie, alebo interpunkcia nie je povolená."
    f"\n**Otázka na klasifikáciu:** \"{OtazkaUzivatela}\""
        )

    split = OtazkaNaGeminiBasic(prompt_text_for_split)
    #print(f"Split:{split}")
    if "Stock" in split:
        print("Stock")
        return Stock(OtazkaUzivatela)
    elif "Komodity" in split:

        print("k")
        return Comodity(OtazkaUzivatela)
    else:
        print("Else")

def Stock(OtazkaUzivatela):
    prompt_text_for_split = (f"Rozdel otazku uzivatela na Nazov stock a medzinarodnu skratku stock. A odpis mi 'Nazov,Skratku'. \nOtazka uzivatela: {OtazkaUzivatela}"
        )
    resp = OtazkaNaGeminiBasic(prompt_text_for_split)
    print(resp)
    Nazov, symbol = resp.split(",")


    return StockPrice.zobraz_cenu(Nazov,symbol)

from .markets import ComodityPrice

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

def main():
    print("Vitaj v komunikacije s Gemini")
    # spýtaj sa používateľa na odpoveď

    user_input = input("Zadaj svoju otazku?")


    # volanie tvojej funkcie AkinatorHra s parametrom
    result = OtazkaUzivatela(user_input)
    # vypíš výsledok
    print("Výsledok:", result)


if __name__ == "__main__":
    main()
