import datetime
import re

# -----------------------------
# Pomocné funkcie pre spracovanie dátumov
# -----------------------------

def parse_date(date_str):
    """Prevedie ISO formát (napr. 2025-10-22T08:24:30Z) na datetime objekt."""
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return None


def _normalize_date_string(date_str):
    """Prekonvertuje formáty '1.6.2024' alebo '2024-06-01' na datetime objekt."""
    for fmt in ("%d.%m.%Y", "%Y-%m-%d"):
        try:
            return datetime.datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Nesprávny formát dátumu: {date_str}")


# -----------------------------
# Filtrovanie podľa rozsahu dátumov
# -----------------------------

def filter_blocks_by_date_ascending(start_date, end_date, blocks):
    """Vracia bloky v rozsahu dátumov od najstaršieho po najnovší."""
    filtered = [
        block for block in blocks
        if (d := parse_date(block["datum_bloku"])) and start_date <= d <= end_date
    ]
    filtered.sort(key=lambda x: parse_date(x["datum_bloku"]))
    return filtered


def filter_blocks_by_date_descending(start_date, end_date, blocks):
    """Vracia bloky v rozsahu dátumov od najnovšieho po najstarší."""
    filtered = [
        block for block in blocks
        if (d := parse_date(block["datum_bloku"])) and start_date <= d <= end_date
    ]
    filtered.sort(key=lambda x: parse_date(x["datum_bloku"]), reverse=True)
    return filtered


# -----------------------------
# Automatická extrakcia dátumového rozsahu z otázky používateľa
# -----------------------------

def extract_date_range_from_text(text: str):
    """
    Analyzuje otázku a vráti (start_date, end_date) ako datetime objekty.
    Podporované formy:
    - 'od 1.6.2024 do 1.1.2025'
    - 'za posledné 3 mesiace'
    - 'za posledný rok'
    - 'za posledné 2 týždne'
    - 'tento mesiac', 'tento rok', 'minulý mesiac'
    """
    text = text.lower()
    today = datetime.datetime.now()

    # -------------------
    # 1️⃣ Absolútne dátumy
    # -------------------
    date_pattern = r"(\d{1,2}\.\d{1,2}\.\d{4})|(\d{4}-\d{2}-\d{2})"
    matches = re.findall(date_pattern, text)

    if matches and len(matches) >= 2:
        # vyber prvé dva dátumy z textu
        flat_dates = [m[0] or m[1] for m in matches]
        start_date = _normalize_date_string(flat_dates[0])
        end_date = _normalize_date_string(flat_dates[1])
        return start_date, end_date

    # -------------------
    # 2️⃣ Relatívne časové obdobia
    # -------------------
    # posledné X mesiacov
    m = re.search(r"posledn(é|y|ych)\s+(\d+)\s+mesiac", text)
    if m:
        months = int(m.group(2))
        start_date = today - datetime.timedelta(days=months * 30)
        return start_date, today

    # posledné X týždňov
    m = re.search(r"posledn(é|y|ych)\s+(\d+)\s+týžd", text)
    if m:
        weeks = int(m.group(2))
        start_date = today - datetime.timedelta(weeks=weeks)
        return start_date, today

    # posledné X dní
    m = re.search(r"posledn(é|y|ych)\s+(\d+)\s+dní|dny", text)
    if m:
        days = int(m.group(2))
        start_date = today - datetime.timedelta(days=days)
        return start_date, today

    # -------------------
    # 3️⃣ Fixné obdobia
    # -------------------
    if "tento mesiac" in text:
        start_date = today.replace(day=1)
        return start_date, today

    if "minulý mesiac" in text:
        first_this_month = today.replace(day=1)
        last_month_end = first_this_month - datetime.timedelta(days=1)
        start_date = last_month_end.replace(day=1)
        return start_date, last_month_end

    if "tento rok" in text:
        start_date = datetime.datetime(today.year, 1, 1)
        return start_date, today

    if "minulý rok" in text:
        start_date = datetime.datetime(today.year - 1, 1, 1)
        end_date = datetime.datetime(today.year - 1, 12, 31)
        return start_date, end_date

    # fallback — ak nič nebolo nájdené, vráť celé obdobie
    return datetime.datetime(1900, 1, 1), today
