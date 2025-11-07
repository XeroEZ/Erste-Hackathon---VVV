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

    prompt_text_for_split = ("Potrebujem rozhodnut co odomna uzivatel ocakava. Ked jeho otazka sa bude tikat Stock tak mi odpis 'Stock', ked sa bude tikat komodit napis 'Komodity' a ked sa bude tikat niecoho ineho odpis 'Ine'"
            f"\nOtazka uzivatela {OtazkaUzivatela}"
        )

    split = OtazkaNaGeminiBasic(prompt_text_for_split)
    #print(f"Split:{split}")
    if "Stock" in split:
        print("Stock")
        return StockPrice(OtazkaUzivatela)
    elif "Komodity" in split:
        print("k")
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
