from . import gemini_main
from . import funkcie
import json
import datetime
import os




def Filtrovanie_podla_kategorie(blocky, categories_skratka, otazka_uzivatela):

    prompt_na_filtrovanie_kategorii = (
        "Si AI asistent pre analýzu dát. Tvojou úlohou je filtrovať zoznam kategórií."
        "\n"
        "\nDostaneš otázku používateľa a zoznam všetkých možných kategórií z databázy."
        "\nVašou úlohou je rozhodnúť, či sa otázka týka **špecifických** kategórií."
        "\n"
        "\n**Pravidlá:**"
        "\n1. Ak sa otázka jasne pýta na určitý druh produktu (napr. 'mäso', 'topánky', 'jedlo', 'alkohol', 'zlozvyky'), vráť Python zoznam **len** s tými kategóriami z pôvodného zoznamu, ktoré sú relevantné."
        "\n2. Ak sa otázka pýta na 'zlozvyky', zváž kategórie ako 'Alkohol', 'Tabak', 'Sladkosti'."
        "\n3. Ak sa otázka **netýka** špecifického typu produktu (napr. pýta sa 'Čo som kúpil včera?', 'Kde som bol?', 'Koľko som minul v Tescu?', 'Aká bola celková suma?'), **MUSÍŠ** vrátiť pôvodný, kompletný zoznam kategórií."
        "\n"
        "\n**Odpoveď musí byť VŽDY iba textový reťazec reprezentujúci Python zoznam (list). Nič iné.**"
        "\n" + ("-" * 30) +
        "\n[ZOZNAM VŠETKÝCH KATEGÓRIÍ]:"
        f"\n{categories_skratka}"
        "\n" + ("-" * 30) +
        "\n[OTÁZKA POUŽÍVATEĽA]:"
        f"\n\"{otazka_uzivatela}\""
        "\n" + ("-" * 30) +
        "\n[FILTROVANÝ ZOZNAM (tvoja odpoveď)]: "
    )

    filtrovane_categorie = gemini_main.OtazkaNaGeminiBasic(prompt_na_filtrovanie_kategorii)
    Good_blocky = funkcie.delete_useless_categories(blocky,filtrovane_categorie) 

    return Good_blocky

def Filtrovanie_podla_casu(blocky, otazka_uzivatela):

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    oldes_time = funkcie.Get_oldes_blocek_time(blocky)
    newest_time = funkcie.Get_newest_blocek_time(blocky)
    
    # returne cas od do
    prompt_na_filtrovania_obdobia = (
        "Si expert na spracovanie dátumov a časových rozmedzí."
        "\n"
        "\n**Tvoja JEDINÁ úloha:** Na základe otázky používateľa urči časové obdobie, na ktoré sa pýta. Tvoja odpoveď musí byť **VŽDY** len samotný JSON objekt s kľúčmi 'start_date' a 'end_date' a **NIČ INÉ**."
        "\n"
        "\n**Dostupné informácie:**"
        f"\n- Dnes je: {today}"
        f"\n- Najstarší záznam v DB je: {oldes_time}"
        f"\n- Najnovší záznam v DB je: {newest_time}"
        "\n"
        "\n**Pravidlá určovania obdobia:**"
        "\n1.  **Formát VÝSTUPU:** Odpoveď musí byť **VŽDY len a len** JSON objekt v tvare: `{\"start_date\": \"YYYY-MM-DDTHH:MM:SSZ\", \"end_date\": \"YYYY-MM-DDTHH:MM:SSZ\"}`. **NEMÔŽE obsahovať žiadny iný text, vysvetlenie ani komentár.**"
        "\n2.  **Konverzia:** Musíš vedieť preložiť výrazy ako 'včera', 'minulý týždeň', 'pred 3 mesiacmi', 'celý rok 2024' na presné dátumy v požadovanom formáte."
        "\n3.  **Nešpecifická otázka:** Ak sa otázka netýka dátumu ani času (napr. 'Koľko ma stáli topánky?', 'Mám psa?'), nastav časové rozmedzie na **celý rozsah databázy**."
        f"\n     V tomto prípade vráť: `\"start_date\": \"{oldes_time}\"` a `\"end_date\": \"{newest_time}\"`."
        "\n4.  **Presnosť:** Dátum/čas musí byť v striktnom ISO 8601 formáte: `YYYY-MM-DDTHH:MM:SSZ`."
        "\n"
        "\n" + ("-" * 40) +
        "\n[OTÁZKA POUŽÍVATEĽA]:"
        f"\n\"{otazka_uzivatela}\""
        "\n" + ("-" * 40)
    )

    reslt = gemini_main.OtazkaNaGeminiBasic(prompt_na_filtrovania_obdobia)
    print(reslt)

    return funkcie.delete_useless_Time(
        blocky,
        oldes_time,
        newest_time
    )



def AI(otazka_uzivatela):

    print("Vitaj v komunikacije s Gemini")
    # spýtaj sa používateľa na odpoveď
    cely_json_string = funkcie.LoadUserDataJson()
    
    # Získanie unikátnych kategórií
    categories_skratka = funkcie.get_categories_list(cely_json_string)
    blocky = funkcie.Replace_multipla_categori(cely_json_string["povodne_ucetnicky"],categories_skratka)

    
    #print(json.dumps(blocky, indent=4, ensure_ascii=False))
    print(f"\nCelkový počet kategórií: {len(categories_skratka)}")


    #print(cely_json_string)
    Blocky_po_filtovani_podla_kategorie = Filtrovanie_podla_kategorie(blocky, categories_skratka, otazka_uzivatela)

    Blocky_po_filtovani_aj_casu = Filtrovanie_podla_casu(Blocky_po_filtovani_podla_kategorie, otazka_uzivatela)
    print(json.dumps(Blocky_po_filtovani_aj_casu, indent=4, ensure_ascii=False))


    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "Good_blocky.json")

    # uloženie do súboru
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(Blocky_po_filtovani_aj_casu, f, indent=4, ensure_ascii=False)

    print(f"✅ Súbor uložený: {file_path}")

    return funkcie.ErikPeknyVipis(Blocky_po_filtovani_aj_casu, funkcie.Get_AllPrice_blocky(Blocky_po_filtovani_aj_casu), otazka_uzivatela)



def main():
    otazka_uzivatela = input("Zadaj svoju otazku? ")
    AI(otazka_uzivatela)
    



if __name__ == "__main__":
    main()