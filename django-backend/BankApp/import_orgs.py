import csv
import os
import django
from datetime import datetime
from django.utils import timezone

# 🔧 Inicializácia Django prostredia
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BankApp.settings")
django.setup()

from core.models import Organization, StoreUnit, Product, Receipt, ReceiptItem
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

# ⚙️ Nastavenia
CSV_PATH = "csvs/receipts.csv"
DEFAULT_USER_ID = 1  # zmeň podľa potreby

print("🚀 Spúšťam import údajov z:", CSV_PATH)

# ------------------------------------------------------------
# 0️⃣ VYPRÁZDNENIE TABULIEK PRED IMPORTON
# ------------------------------------------------------------
print("🧹 Vyprazdňujem tabuľky pred importom...")

# Vymazanie v správnom poradí kvôli cudzím kľúčom
ReceiptItem.objects.all().delete()
print("✅ Vymazané všetky ReceiptItem")

Receipt.objects.all().delete()
print("✅ Vymazané všetky Receipt")

StoreUnit.objects.all().delete()
print("✅ Vymazané všetky StoreUnit")

Product.objects.all().delete()
print("✅ Vymazané všetky Product")

Organization.objects.all().delete()
print("✅ Vymazané všetky Organization")

print("🎯 Tabuľky boli úspešne vyprázdnené, začínam import...")

# ------------------------------------------------------------
# 1️⃣ HLAVNÝ IMPORT
# ------------------------------------------------------------
with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    count = 0

    for row in reader:
        try:
            # === ORGANIZÁCIA ===
            org, org_created = Organization.objects.get_or_create(
                organization_id=row.get("org_id"),
                defaults={
                    "name": row.get("org_name") or "Neznáma organizácia",
                    "ico": row.get("org_ico") or None,
                    "dic": row.get("org_dic") or None,
                    "ic_dph": row.get("org_ic_dph") or None,
                    "country": row.get("org_country") or "Slovensko",
                    "municipality": row.get("org_municipality") or None,
                    "postal_code": row.get("org_postal_code") or None,
                    "street_name": row.get("org_street_name") or None,
                    "building_number": row.get("org_building_number") or None,
                }
            )
            print(f"{'🆕' if org_created else 'ℹ️'} Organizácia: {org.name}")

            # === STORE UNIT ===
            unit, unit_created = StoreUnit.objects.get_or_create(
                unit_id=row.get("unit_id"),
                defaults={
                    "organization": org,
                    "name": row.get("unit_name") or None,
                    "country": row.get("unit_country") or "Slovensko",
                    "municipality": row.get("unit_municipality") or None,
                    "postal_code": row.get("unit_postal_code") or None,
                    "street_name": row.get("unit_street_name") or None,
                    "building_number": row.get("unit_building_number") or None,
                    "property_registration_number": row.get("unit_property_registration_number") or None,
                    "latitude": row.get("unit_latitude") or None,
                    "longitude": row.get("unit_longitude") or None,
                }
            )
            print(f"{'🏢🆕' if unit_created else '🏢'} Jednotka: {unit.name or '(bez názvu)'}")

            # === USER ===
            user = User.objects.filter(id=DEFAULT_USER_ID).first()
            if not user:
                print("❌ Chýba používateľ pre import (nastav DEFAULT_USER_ID).")
                break

            # === RECEIPT ===
            receipt, receipt_created = Receipt.objects.get_or_create(
                fs_receipt_id=row.get("fs_receipt_id"),
                defaults={
                     "issue_date": timezone.make_aware(
                        datetime.fromisoformat(
                            row.get("fs_receipt_issue_date").split(" +")[0]
                        )
                    ) if row.get("fs_receipt_issue_date") else None,
                    "organization": org,
                    "store_unit": unit,
                    "user": user,
                    "total_price": row.get("price") or None,
                }
            )
            print(f"{'🧾🆕' if receipt_created else '🧾'} Receipt: {receipt.fs_receipt_id}")

            # === PRODUCT ===
            product_name = row.get("name") or row.get("ai_name_without_brand_and_quantity") or "Neznámy produkt"
            product, product_created = Product.objects.get_or_create(
                name=product_name,
                defaults={
                    "original_name": row.get("name") or None,
                    "brand": row.get("ai_brand") or None,
                    "category": row.get("ai_category") or None,
                    "ai_category": row.get("ai_category") or None,
                    "ai_name": row.get("ai_name_without_brand_and_quantity") or None,
                    "ai_name_english": row.get("ai_name_in_english_without_brand_and_quantity") or None,
                }
            )
            print(f"{'📦🆕' if product_created else '📦'} Produkt: {product.name}")

            # === RECEIPT ITEM ===
            ReceiptItem.objects.create(
                receipt=receipt,
                product=product,
                quantity=row.get("quantity") or 1,
                unit_price=row.get("price") or 0,
                total_price=row.get("price") or 0,
                ai_name_without_brand=row.get("ai_name_without_brand_and_quantity") or None,
                ai_name_english=row.get("ai_name_in_english_without_brand_and_quantity") or None,
                ai_brand=row.get("ai_brand") or None,
                ai_category=row.get("ai_category") or None,
                ai_quantity_value=row.get("ai_quantity_value") or None,
                ai_quantity_unit=row.get("ai_quantity_unit") or None,
            )
            print("   ➕ Pridaná položka do účtenky")

            count += 1

            # 👇 voliteľne: zobraz len prvých pár riadkov
            if count % 10 == 0:
                print(f"--- Spracovaných {count} riadkov ---")

        except Exception as e:
            print(f"⚠️ Chyba pri riadku id={row.get('id')}: {e}")
            continue

print(f"\n✅ Hotovo — úspešne spracovaných {count} riadkov z {CSV_PATH}")