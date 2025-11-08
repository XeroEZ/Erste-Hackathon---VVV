from . import gemini_main
from . import funkcie
from . import funkcie_2
import json
import datetime
import os


def main():
    print("Vitaj v komunikácii s Gemini")

    #Načítanie databázy
    cely_json_string = funkcie.LoadUserDataJson()
    povodne_blocky = cely_json_string["povodne_ucetnicky"]

    #Získanie kategórií
    categories_skratka = funkcie.get_categories_list(cely_json_string)
    blocky = funkcie.Replace_multipla_categori(povodne_blocky, categories_skratka)
    print(f"\nCelkový počet kategórií: {len(categories_skratka)}")

    #Otázka používateľa
    otazka_uzivatela = input("Zadaj svoju otázku: ")

    #AI prompt na vyhodnotenie časového rozmedzia
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    prompt_cas = f"""
Si AI asistent pre analýzu dát. Tvojou úlohou je určiť presný časový rozsah,
ktorý používateľ svojou otázkou myslí.

🧠 Pravidlá:
1. Ak otázka obsahuje konkrétne dátumy (napr. "od 1.6.2024 do 1.1.2025"), vráť ich ako rozsah.
2. Ak obsahuje relatívny čas (napr. "za posledné 3 mesiace", "tento rok", "minulý týždeň"),
   prepočítaj na presné dátumy.
3. Ak otázka neobsahuje žiadny časový údaj, nastav celé obdobie (1900-01-01 až dnešný dátum).
4. Dnešný dátum je: {today}
5. Odpoveď musí byť **IBA** Python zoznam dvoch dátumov v ISO formáte (YYYY-MM-DD).
   Príklad: ["2024-06-01", "2025-01-01"]

----------------------------------------
[OTÁZKA POUŽÍVATEĽA]:
"{otazka_uzivatela}"
----------------------------------------
[ODPOVEĎ - časové rozmedzie]:
"""

    odpoved_cas = gemini_main.OtazkaNaGeminiBasic(prompt_cas).strip()

    try:
        date_list = json.loads(odpoved_cas.replace("'", '"'))
        start_date = datetime.datetime.strptime(date_list[0], "%Y-%m-%d")
        end_date = datetime.datetime.strptime(date_list[1], "%Y-%m-%d")
    except Exception:
        print("AI nevrátilo správny formát dátumu. Používam celé obdobie.")
        start_date = datetime.datetime(1900, 1, 1)
        end_date = datetime.datetime.now()

    print(f"\nRozpoznané obdobie: {start_date.date()} – {end_date.date()}")

    #Filtrovanie blokov podľa dátumu
    filtrované_blocky = funkcie_2.filter_blocks_by_date_descending(start_date, end_date, blocky)
    print(f"Počet blokov v období: {len(filtrované_blocky)}")

    #AI prompt na filtrovanie kategórií
    prompt_kategorie = (
        "Si AI asistent pre analýzu dát. Tvojou úlohou je filtrovať zoznam kategórií.\n"
        "Dostaneš otázku používateľa a zoznam všetkých možných kategórií z databázy.\n"
        "Vašou úlohou je rozhodnúť, či sa otázka týka **špecifických** kategórií.\n\n"
        "🔹 Pravidlá:\n"
        "1. Ak sa otázka jasne pýta na určitý druh produktu (napr. 'mäso', 'topánky', 'jedlo', 'alkohol', 'zlozvyky'), "
        "vráť Python zoznam **len** s tými kategóriami z pôvodného zoznamu, ktoré sú relevantné.\n"
        "2. Ak sa otázka pýta na 'zlozvyky', zváž kategórie ako 'Alkohol', 'Tabak', 'Sladkosti'.\n"
        "3. Ak sa otázka netýka špecifického typu produktu (napr. 'čo som kúpil včera', 'koľko som minul', 'čo som kúpil v Tescu'), "
        "vráť pôvodný kompletný zoznam kategórií.\n\n"
        "**Odpoveď musí byť VŽDY iba Python zoznam (list). Nič iné.**\n"
        + "-" * 30 +
        f"\n[ZOZNAM VŠETKÝCH KATEGÓRIÍ]:\n{categories_skratka}\n"
        + "-" * 30 +
        f"\n[OTÁZKA POUŽÍVATEĽA]:\n\"{otazka_uzivatela}\"\n"
        + "-" * 30 +
        "\n[FILTROVANÝ ZOZNAM (tvoja odpoveď)]: "
    )

    odpoved_kategorie = gemini_main.OtazkaNaGeminiBasic(prompt_kategorie).strip()

    try:
        relevantne_kategorie = json.loads(odpoved_kategorie.replace("'", '"'))
    except Exception:
        print("⚠️ AI nevrátilo platný Python list kategórií. Používam všetky.")
        relevantne_kategorie = categories_skratka

    print(f"🏷️ Filtrované kategórie: {relevantne_kategorie}")

    #Optimalizované dáta – pošli len prehľad, nie celý JSON
    zhrnutie = []
    for blok in filtrované_blocky:
        datum = blok.get("datum_bloku")
        obchod = blok.get("obchod", "Neznámy obchod")
        polozky = blok.get("polozky", [])
        nazvy_poloziek = [p.get("nazov", "") for p in polozky]
        kategorie = list({p.get("shortCategoris") for p in polozky if p.get("shortCategoris")})
        zhrnutie.append({
            "datum": datum,
            "obchod": obchod,
            "pocet_poloziek": len(nazvy_poloziek),
            "kategorie": kategorie
        })

    # Ak je príliš veľa blokov, obmedz výstup (napr. 50)
    if len(zhrnutie) > 50:
        zhrnutie = zhrnutie[:50]

    #Finálny prompt pre AI odpoveď
    prompt_final = (
        "Si AI asistent pre analýzu osobných nákupov.\n"
        "Na základe otázky, časového obdobia a kategórií zhrň odpoveď v slovenskej reči.\n\n"
        f"[OTÁZKA]: {otazka_uzivatela}\n"
        f"[OBDOBIE]: {start_date.date()} – {end_date.date()}\n"
        f"[KATEGÓRIE]: {relevantne_kategorie}\n"
        "----------------------------------------\n"
        "Tu sú sumarizované bloky (obchod, dátum, kategórie):\n"
        f"{json.dumps(zhrnutie, indent=2, ensure_ascii=False)}\n"
        "----------------------------------------\n"
        "Odpovedz stručne, prehľadne a po slovensky. "
        "Zhrň, čo si používateľ kúpil, prípadne v ktorých obchodoch a aké typy produktov prevažovali.\n"
    )

    final_result = gemini_main.OtazkaNaGeminiBasic(prompt_final)

    print("\nVýsledok :")
    print(final_result)


if __name__ == "__main__":
    main()
