from . import geminiKey

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
        return StockPrice(OtazkaUzivatela)
    elif "Komodity" in split:

        print("k")
        return StockPrice(OtazkaUzivatela)
    else:
        print("Else")

def StockPrice(OtazkaUzivatela):
    prompt_text_for_split = (f"Rozdel otazku uzivatela na Nazov stock a medzinarodnu skratku stock. A odpis mi 'Nazov,Skratku'. \nOtazka uzivatela: {OtazkaUzivatela}"
        )
    resp = OtazkaNaGeminiBasic(prompt_text_for_split)

    return resp






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
