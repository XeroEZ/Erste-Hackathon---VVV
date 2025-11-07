from . import gemini_main
from . import funkcie
import json
import os






def main():
    print("Vitaj v komunikacije s Gemini")
    # spýtaj sa používateľa na odpoveď
    cely_json_string = funkcie.LoadUserDataJson()
    
    # Získanie unikátnych kategórií
    categories_skratka = funkcie.get_categories_list(cely_json_string)
    #print(categories_skratka)
    # Výpis výsledkov

    blocky = funkcie.Replace_multipla_categori(cely_json_string["povodne_ucetnicky"],categories_skratka)
    #print(json.dumps(blocky, indent=4, ensure_ascii=False))
    print(f"\nCelkový počet kategórií: {len(categories_skratka)}")
    return


    #print(cely_json_string)

    otazka_uzivatela = input("Zadaj svoju otazku? ")

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
        f"\n{categories}"
        "\n" + ("-" * 30) +
        "\n[OTÁZKA POUŽÍVATEĽA]:"
        f"\n\"{otazka_uzivatela}\""
        "\n" + ("-" * 30) +
        "\n[FILTROVANÝ ZOZNAM (tvoja odpoveď)]: "
    )

    result = gemini_main.OtazkaNaGeminiBasic(prompt_na_filtrovanie_kategorii)
    # vypíš výsledok
    print("Výsledok: ", result)




if __name__ == "__main__":
    main()