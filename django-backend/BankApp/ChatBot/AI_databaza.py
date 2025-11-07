from . import gemini_main
import json
import os

def LoadUserDataJson():
    # Absolútna cesta k aktuálnemu adresáru tohto súboru
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Cesta k súboru user_data.json
    data_path = os.path.join(BASE_DIR, "user_data.json")

    # Načítanie JSON dát
    with open(data_path, "r", encoding="utf-8") as f:
        user_data = json.load(f)

    return user_data
    #print(user_data["username"])


Json_Format = {
  "type": "object",
  "properties": {
    "user_id": { "type": "integer" },
    "username": { "type": "string" },
    "pocet_povodnych_ucetniok": { "type": "integer" },
    "povodne_ucetnicky": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id_bloku": { "type": "string" },
          "datum_bloku": { "type": "string", "format": "date-time" },
          "celkova_suma": { "type": "number" },
          "organizacia": {
            "type": "object",
            "properties": {
              "nazov": { "type": ["string","null"] },
              "ico": { "type": ["string","null"] }
            }
          },
          "pobocka": {
            "type": "object",
            "properties": {
              "nazov": { "type": ["string","null"] },
              "adresa": { "type": ["string","null"] },
              "mesto": { "type": ["string","null"] }
            }
          },
          "polozky": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "nazov_produktu": { "type": "string" },
                "ai_nazov": { "type": ["string","null"] },
                "mnozstvo": { "type": "number" },
                "jednotkova_cena": { "type": "number" },
                "celkova_cena_polozky": { "type": "number" },
                "znacka": { "type": ["string","null"] },
                "kategoria": { "type": ["string","null"] }
              },
              "required": ["nazov_produktu","mnozstvo","jednotkova_cena","celkova_cena_polozky"]
            }
          }
        },
        "required": ["id_bloku","datum_bloku","celkova_suma","organizacia","pobocka","polozky"]
      }
    }
  },
  "required": ["user_id","username","pocet_povodnych_ucetniok","povodne_ucetnicky"]
}

def main():
    print("Vitaj v komunikacije s Gemini")
    # spýtaj sa používateľa na odpoveď
    cely_json_string = LoadUserDataJson()

    #print(cely_json_string)

    otazka_uzivatela = input("Zadaj svoju otazku? ")

    
    # volanie tvojej funkcie AkinatorHra s parametrom
    prompt_text_pre_AI = (
        "Ste expertný AI asistent pre analýzu dát. Vašou úlohou je odpovedať na otázku používateľa."
        "\nAko zdroj dát môžete použiť **iba** nižšie poskytnutú JSON databázu."
        "\n" + ("-" * 30) +
        "\n[JSON DATABÁZA]:"
        f"\n```json\n{cely_json_string}\n```"
        "\n" + ("-" * 30) +
        "\n[OTÁZKA POUŽÍVATEĽA]:"
        f"\n\"{otazka_uzivatela}\""
        "\n" + ("-" * 30) +
        "\n[INŠTRUKCIE PRE VAŠU ODPOVEĎ]:"
        "\n1. **Analyzujte otázku:** Zistite, čo presne sa používateľ pýta (časové obdobie, kategória produktu, celková suma, konkrétne položky)."
        "\n2. **Prehľadajte JSON:** Starostlivo prehľadajte dáta v JSON databáze. Kľúčové polia sú `povodne_ucetnicky`, `datum_bloku`, `polozky`, `polozky.ai_nazov`, `polozky.kategoria` a `polozky.celkova_cena_polozky`."
        "\n3. **Formulujte odpoveď:**"
        "\n   - **Musíte** odpovedať **výhradne** na základe dát v JSONe."
        "\n   - Ak sa otázka pýta na niečo, čo v JSONe **nie je** (napr. 'Koľko členov má moja rodina?'), odpovedzte: 'Túto informáciu v mojej databáze účteniek nemám.'"
        "\n   - Ak sa otázka pýta na niečo, čo sa dá z dát **odvodiť** (npr. 'Mám psa?' alebo 'Kde bývam?'), odpovedzte na základe dôkazov z nákupov, ale jasne uveďte, že ide o **predpoklad**. (Príklad: 'Neviem to naisto, ale vidím, že pravidelne kupuješ granule pre psa, takže je to pravdepodobné.')"
        "\n"
        "\nZačnite priamo odpoveďou na otázku používateľa."
    )


    result = gemini_main.OtazkaNaGeminiBasic(prompt_text_pre_AI)
    # vypíš výsledok
    print("Výsledok:", result)


if __name__ == "__main__":
    main()