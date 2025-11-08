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
    


def get_categories_list(user_data):
    categories = set()
    
    for block in user_data["povodne_ucetnicky"]:
        for item in block["polozky"]:
            category = item["kategoria"]
            if category:
                # Normalizácia - malé písmená, odstránenie medzier
                normalized_category = category.strip().lower()
                categories.add(normalized_category)
    
    # Odstránenie duplikátov množného čísla
    final_categories = remove_plural_duplicates(categories)
    
    return sorted(list(final_categories))

def remove_plural_duplicates(categories):
    """Odstráni duplikáty kde jedna kategória je množné číslo druhej"""
    categories_list = sorted(list(categories))
    to_remove = set()
    
    plural_rules = [
        ('s', ''),           # yogurts -> yogurt
        ('es', ''),          # boxes -> box
        ('ies', 'y'),        # cookies -> cookie
    ]
    
    for category in categories_list:
        for pattern, replacement in plural_rules:
            if category.endswith(pattern):
                singular = category[:-len(pattern)] + replacement
                if singular in categories_list:
                    to_remove.add(category)
                    break
    
    return categories - to_remove

from rapidfuzz import fuzz

def fuzzmatch(input1: str, input2: str) -> float:
    best_similarity = fuzz.token_sort_ratio(input1, input2.title())
    return best_similarity

def Replace_multipla_categori(InputBlocky, Categoris):
    for blocek in InputBlocky:

        for polozka in blocek["polozky"]:
            bestmatch = {}
            #print(polozka["kategoria"])
            if polozka["kategoria"] is None:
                polozka["shortCategoris"] = None
                continue

            for cat in Categoris:

                percenta = fuzzmatch(polozka["kategoria"], cat)
                if not bestmatch or (bestmatch and bestmatch["percent"] < percenta):
                    bestmatch["percent"] = percenta
                    bestmatch["category"] = cat

            polozka["shortCategoris"] = bestmatch["category"]

    return InputBlocky

def delete_useless_categories(InputBlocky, Categoris):
    """Odstráni položky, ktorých shortCategoris nie je v povolených kategóriách."""
    cleaned_blocks = []

    for blocek in InputBlocky:
        # použijeme nový zoznam, aby sme bezpečne odstránili položky
        new_items = []

        for polozka in blocek["polozky"]:
            short_cat = polozka.get("shortCategoris")

            # preskočí položky bez kategórie
            if short_cat is None:
                continue

            # ak shortCategoris je povolená, necháme ju
            if short_cat in Categoris:
                new_items.append(polozka)

        # len ak po filtrovaní nie je bloček prázdny, pridáme ho späť
        if new_items:
            blocek["polozky"] = new_items
            cleaned_blocks.append(blocek)

    return cleaned_blocks
            

from datetime import datetime

def Get_oldes_blocek_time(blocky):
    """Vráti najstarší dátum bločku (datum_bloku) vo formáte 'YYYY-MM-DDTHH:MM:SSZ'."""
    oldes_time = None

    for blocek in blocky:
        datum_str = blocek.get("datum_bloku")

        if not datum_str:
            continue

        try:
            # 'Z' -> UTC
            datum = datetime.fromisoformat(datum_str.replace("Z", "+00:00"))
        except ValueError:
            continue

        if oldes_time is None or datum < oldes_time:
            oldes_time = datum

    return oldes_time.strftime("%Y-%m-%dT%H:%M:%SZ") if oldes_time else None


def Get_newest_blocek_time(blocky):
    """Vráti najnovší dátum bločku (datum_bloku) vo formáte 'YYYY-MM-DDTHH:MM:SSZ'."""
    newest_time = None

    for blocek in blocky:
        datum_str = blocek.get("datum_bloku")
        if not datum_str:
            continue

        try:
            datum = datetime.fromisoformat(datum_str.replace("Z", "+00:00"))
        except ValueError:
            continue

        if newest_time is None or datum > newest_time:
            newest_time = datum

    return newest_time.strftime("%Y-%m-%dT%H:%M:%SZ") if newest_time else None

def delete_useless_Time(InputBlocky, start_date, end_date):
    """Odstráni položky, ktorých shortCategoris nie je v povolených kategóriách."""
    cleaned_blocks = []

    for blocek in InputBlocky:
        if start_date <= blocek["datum_bloku"] and blocek["datum_bloku"] <= end_date:
            cleaned_blocks.append(blocek)


    return cleaned_blocks


def Get_AllPrice_blocky(blocky):
    celkova_cena = 0
    for blocek in blocky:
        for polozka in blocek["polozky"]:
            celkova_cena += polozka["celkova_cena_polozky"] * polozka["mnozstvo"]

    return round(celkova_cena, 2)


def ErikPeknyVipis(blocky, celkova_cena):
    print("ppp")
    return f"Celova cena {celkova_cena}"
    return None
