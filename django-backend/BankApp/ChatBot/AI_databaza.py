from . import gemini_main
from . import funkcie
import json
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



def main():
    print("Vitaj v komunikacije s Gemini")
    # spýtaj sa používateľa na odpoveď
    cely_json_string = funkcie.LoadUserDataJson()
    
    # Získanie unikátnych kategórií
    categories_skratka = funkcie.get_categories_list(cely_json_string)
    blocky = funkcie.Replace_multipla_categori(cely_json_string["povodne_ucetnicky"],categories_skratka)

    #print(json.dumps(blocky, indent=4, ensure_ascii=False))
    print(f"\nCelkový počet kategórií: {len(categories_skratka)}")


    #print(cely_json_string)

    otazka_uzivatela = input("Zadaj svoju otazku? ")
    Good_blocky = Filtrovanie_podla_kategorie(blocky, categories_skratka, otazka_uzivatela)

    #print(json.dumps(Good_blocky, indent=4, ensure_ascii=False))


    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "Good_blocky.json")

    # uloženie do súboru
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(Good_blocky, f, indent=4, ensure_ascii=False)

    print(f"✅ Súbor uložený: {file_path}")




if __name__ == "__main__":
    main()