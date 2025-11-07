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