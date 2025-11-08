from . import gemini_main
from . import funkcie
import json
import datetime
import os


def Filtrovanie_podla_kategorie(blocky, categories_skratka, otazka_uzivatela):
    prompt_na_filtrovanie_kategorii = (
            "Si AI asistent pre analýzu dát. Tvojou úlohou je filtrovať zoznam kategórií."
            "\nDostaneš otázku používateľa a zoznam všetkých možných kategórií z databázy."
            "\nVašou úlohou je rozhodnúť, či sa otázka týka **špecifických** kategórií."
            "\n\n**Pravidlá:**"
            "\n1. Ak sa otázka jasne pýta na určitý druh produktu (napr. 'mäso', 'topánky', 'jedlo', 'alkohol', 'zlozvyky'), vráť Python zoznam **len** s tými kategóriami z pôvodného zoznamu, ktoré sú relevantné."
            "\n2. Ak sa otázka pýta na 'zlozvyky', zváž kategórie ako 'Alkohol', 'Tabak', 'Sladkosti'."
            "\n3. Ak sa otázka **netýka** špecifického typu produktu (napr. pýta sa 'Čo som kúpil včera?', 'Kde som bol?', 'Koľko som minul v Tescu?', 'Aká bola celková suma?'), **MUSÍŠ** vrátiť pôvodný, kompletný zoznam kategórií."
            "\n\n**Odpoveď musí byť VŽDY iba textový reťazec reprezentujúci Python zoznam (list). Nič iné.**"
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
    Good_blocky = funkcie.delete_useless_categories(blocky, filtrovane_categorie)
    return Good_blocky


def Filtrovanie_podla_casu(blocky, otazka_uzivatela):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    oldes_time = funkcie.Get_oldes_blocek_time(blocky)
    newest_time = funkcie.Get_newest_blocek_time(blocky)

    prompt_na_filtrovania_obdobia = (
            "Si expert na spracovanie dátumov a časových rozmedzí."
            "\n**Tvoja JEDINÁ úloha:** Na základe otázky používateľa urči časové obdobie, na ktoré sa pýta."
            "\nOdpoveď musí byť **VŽDY** len samotný JSON objekt s kľúčmi 'start_date' a 'end_date' a **NIČ INÉ**."
            "\n\n**Dostupné informácie:**"
            f"\n- Dnes je: {today}"
            f"\n- Najstarší záznam v DB je: {oldes_time}"
            f"\n- Najnovší záznam v DB je: {newest_time}"
            "\n\n**Pravidlá určovania obdobia:**"
            f"\n1.  Formát výstupu: {{\"start_date\": \"YYYY-MM-DDTHH:MM:SSZ\", \"end_date\": \"YYYY-MM-DDTHH:MM:SSZ\"}}."
            f"\n2.  Ak sa otázka netýka času, použij celý rozsah databázy."
            f"\n3.  Ak sa pýta na 'včera', 'minulý týždeň', 'tento rok', prelož to na presné dátumy."
            "\n" + ("-" * 40) +
            "\n[OTÁZKA POUŽÍVATEĽA]:"
            f"\n\"{otazka_uzivatela}\""
            "\n" + ("-" * 40)
    )

    reslt = gemini_main.OtazkaNaGeminiBasic(prompt_na_filtrovania_obdobia)
    print(reslt)

    return funkcie.delete_useless_Time(blocky, oldes_time, newest_time)


def AI(otazka_uzivatela):
    print("Vitaj v komunikácii s Gemini")
    cely_json_string = funkcie.LoadUserDataJson()

    categories_skratka = funkcie.get_categories_list(cely_json_string)
    blocky = funkcie.Replace_multipla_categori(
        cely_json_string["povodne_ucetnicky"], categories_skratka
    )

    # Najprv skús zistiť, či otázka vôbec súvisí s databázou
    kontrolny_prompt = (
        "Si klasifikačný model. Tvojou úlohou je rozhodnúť, či otázka používateľa "
        "súvisí s osobnými nákupmi, výdavkami, kategóriami produktov alebo časom (napr. 'čo som kúpil', 'koľko som minul', 'v Tescu', 'tento mesiac').\n"
        "Ak áno, odpíš presne 'nakupy'.\n"
        "Ak sa otázka netýka týchto tém (napr. 'mám psa', 'koľko mám rokov', 'kto som'), odpíš presne 'nenakupne'.\n"
        f"\nOtázka: \"{otazka_uzivatela}\""
    )

    klasifikacia = gemini_main.OtazkaNaGeminiBasic(kontrolny_prompt).lower().strip()
    print(f"Klasifikácia otázky: {klasifikacia}")

    # Ak otázka NESÚVISÍ s databázou, odpovedz normálne
    if "nenakupne" in klasifikacia:
        odpoved_mimo = (
            "Si asistent pre finančnú aplikáciu. Tvoja úloha je reagovať na otázku používateľa, ktorá nesúvisí s dátami o jeho transakciách."
            "\n"
            "\n**DÁTA K DISPOZÍCII:**"
            "\n- Máš k dispozícii **iba** informácie o finančných transakciách, nákupoch, cenách a dátumoch (transakčné dáta)."
            f"\n- **Otázka používateľa:** \"{otazka_uzivatela}\""
            "\n"
            "\n**POKYNY PRE ODPOVEĎ (Výsledok AI):**"
            "\n1.  **Tón:** Použi **profesionálny, vecný a zdvorilý tón** bankového asistenta. Komunikuj v slovenčine."
            "\n2.  **Odpoveď:** Vysvetli používateľovi, že tvoja funkcia je obmedzená len na spracovanie a analýzu **finančných transakcií** a nemôžeš odpovedať na otázky, ktoré presahujú tieto dáta."
            "\n3.  **Jasnosť:** Odpoveď by mala byť krátka, priama a uistená. Vyhni sa ospravedlňovaniu alebo zbytočnému zmäkčovaniu."
            "\n4.  **Čistota výstupu:** Tvoja odpoveď musí byť len samotný text pre používateľa, bez akýchkoľvek úvodných fráz a bez špeciálnych znakov (ako `*` alebo `#`)."
            "\n"
            "\n[ŽIADANÁ ODPOVEĎ (začni rovno textom pre používateľa)]: "
        )
        return gemini_main.OtazkaNaGeminiBasic(odpoved_mimo)

    # 🛒 Ak otázka súvisí s nákupmi, pokračuj ako doteraz
    Blocky_po_filtrovani_kategorie = Filtrovanie_podla_kategorie(
        blocky, categories_skratka, otazka_uzivatela
    )

    Blocky_po_filtrovani_casu = Filtrovanie_podla_casu(
        Blocky_po_filtrovani_kategorie, otazka_uzivatela
    )

    return funkcie.ErikPeknyVipis(
        Blocky_po_filtrovani_casu,
        funkcie.Get_AllPrice_blocky(Blocky_po_filtrovani_casu),
        otazka_uzivatela
    )


def main():
    otazka_uzivatela = input("Zadaj svoju otázku: ")
    print(AI(otazka_uzivatela))


if __name__ == "__main__":
    main()
