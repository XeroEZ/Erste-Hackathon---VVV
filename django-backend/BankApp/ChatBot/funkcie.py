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

def delete_useless_categories
    

        


#def filtrovanie_kategorii_z_blockou(blocky):
