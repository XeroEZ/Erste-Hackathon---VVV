from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatSession, ChatMessage
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product

from .models import Receipt

from rest_framework.decorators import api_view, permission_classes
from django.db.models import Count
from django.contrib.auth.models import User


class ProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.all().values()
        return Response(list(products))


@login_required
def start_chat(request):
    """Vytvorí novú chat reláciu pre aktuálneho používateľa."""
    session = ChatSession.objects.create(user=request.user)
    return JsonResponse({"session_id": session.id})


@csrf_exempt
def send_message(request, session_id):
    if request.method == "POST":
        text = request.POST.get("message")
        session = get_object_or_404(ChatSession, id=session_id)

        ChatMessage.objects.create(session=session, sender='user', message=text)

        # Tu by si neskôr volal AI logiku
        bot_reply = f"Odpoveď na '{text}'"
        ChatMessage.objects.create(session=session, sender='bot', message=bot_reply)

        return JsonResponse({"user": text, "bot": bot_reply})
    return JsonResponse({"error": "Invalid method"}, status=405)


@login_required
def get_chat_history(request, session_id):
    """Získanie histórie konverzácie pre danú reláciu."""
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    messages = session.messages.order_by("created_at").values("sender", "message", "created_at")
    return JsonResponse(list(messages), safe=False)


def get_receipt_content(fs_receipt_id):
    try:
        receipt = Receipt.objects.select_related(
            'organization', 
            'store_unit'
        ).prefetch_related(
            'items__product'
        ).get(fs_receipt_id=fs_receipt_id)
        
        receipt_data = {
            'receipt_id': receipt.fs_receipt_id,
            'issue_date': receipt.issue_date,
            'total_price': float(receipt.total_price) if receipt.total_price else 0,
            'organization': {
                'name': receipt.organization.name,
                'ico': receipt.organization.ico,
                'address': f"{receipt.organization.street_name or ''} {receipt.organization.building_number or ''}".strip(),
                'city': receipt.organization.municipality,
                'postal_code': receipt.organization.postal_code
            },
            'store_unit': None,
            'items': []
        }
        
        if receipt.store_unit:
            receipt_data['store_unit'] = {
                'name': receipt.store_unit.name,
                'address': f"{receipt.store_unit.street_name or ''} {receipt.store_unit.building_number or ''}".strip(),
                'city': receipt.store_unit.municipality,
                'postal_code': receipt.store_unit.postal_code
            }
        
        for item in receipt.items.all():
            receipt_data['items'].append({
                'product_name': item.product.name,
                'ai_name': item.ai_name_without_brand,
                'quantity': float(item.quantity),
                'unit_price': float(item.unit_price),
                'total_price': float(item.total_price),
                'brand': item.ai_brand,
                'category': item.ai_category
            })
        
        return receipt_data
    
    except Receipt.DoesNotExist:
        return None


def receipt_detail_api(request, fs_receipt_id):
    """API endpoint for JSON response"""
    receipt_data = get_receipt_content(fs_receipt_id)
    
    if receipt_data is None:
        return JsonResponse(
            {'error': f'Receipt {fs_receipt_id} not found'}, 
            status=404
        )
    
    return JsonResponse(receipt_data)


def receipt_detail_page(request, fs_receipt_id):
    """HTML page for receipt details"""
    receipt_data = get_receipt_content(fs_receipt_id)
    
    if receipt_data is None:
        return render(request, 'core/receipt_not_found.html', {
            'receipt_id': fs_receipt_id
        }, status=404)
    
    return render(request, 'core/receipt_detail.html', {
        'receipt': receipt_data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def public_total_store_visits(request, user_id):
    """
    Verejný endpoint pre celkový počet návštev podľa user_id
    """
    user = get_object_or_404(User, id=user_id)
    total_visits = Receipt.objects.filter(user=user).count()
    
    return Response({
        'user_id': user.id,
        'username': user.username,
        'total_store_visits': total_visits
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def public_store_visits_breakdown(request, user_id):
    """
    Verejný endpoint pre prehľad návštev podľa user_id
    """
    user = get_object_or_404(User, id=user_id)
    
    store_visits = Receipt.objects.filter(user=user)\
        .select_related('store_unit', 'organization')\
        .values(
            'store_unit__unit_id',
            'organization__name',  # ✅ ZMENENÉ: store_unit__name -> organization__name
            'store_unit__street_name',
            'store_unit__building_number', 
            'store_unit__municipality'
        )\
        .annotate(visit_count=Count('receipt_id'))\
        .order_by('-visit_count')
    
    # Formátovanie výstupu
    formatted_visits = []
    for visit in store_visits:
        organization_name = visit['organization__name'] or "Neznáma organizácia"  # ✅ ZMENENÉ
        address = f"{visit['store_unit__street_name'] or ''} {visit['store_unit__building_number'] or ''}".strip()
        city = visit['store_unit__municipality'] or ""
        
        formatted_visits.append({
            'store_id': visit['store_unit__unit_id'],
            'organizacia': organization_name,  # ✅ ZMENENÉ: store_name -> organizacia
            'adresa': address,  # ✅ ZMENENÉ: address -> adresa
            'mesto': city,  # ✅ ZMENENÉ: city -> mesto
            'pocet_navstev': visit['visit_count']  # ✅ ZMENENÉ: visit_count -> pocet_navstev
        })
    
    total_visits = sum(visit['visit_count'] for visit in store_visits)
    
    return Response({
        'user_id': user.id,
        'username': user.username,
        'celkovy_pocet_navstev': total_visits,  # ✅ ZMENENÉ: total_visits -> celkovy_pocet_navstev
        'pocet_navstivenych_pobociek': len(formatted_visits),  # ✅ ZMENENÉ: stores_visited -> pocet_navstivenych_pobociek
        'prehlad': formatted_visits  # ✅ ZMENENÉ: breakdown -> prehlad
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def public_user_visit_statistics(request, user_id):
    """
    Verejný endpoint pre kompletné štatistiky podľa user_id
    """
    user = get_object_or_404(User, id=user_id)
    receipts = Receipt.objects.filter(user=user)
    
    total_visits = receipts.count()
    
    # Návštevy podľa pobočiek
    store_visits = receipts\
        .select_related('store_unit')\
        .values(
            'store_unit__unit_id',
            'store_unit__name',
            'store_unit__street_name',
            'store_unit__building_number',
            'store_unit__municipality'
        )\
        .annotate(visit_count=Count('receipt_id'))\
        .order_by('-visit_count')
    
    # Návštevy podľa organizácií
    org_visits = receipts\
        .select_related('organization')\
        .values('organization__name')\
        .annotate(visit_count=Count('receipt_id'))\
        .order_by('-visit_count')
    
    # Najobľúbenejšia pobočka
    favorite_store = store_visits.first() if store_visits else None
    favorite_org = org_visits.first() if org_visits else None
    
    return Response({
        'user_id': user.id,
        'username': user.username,
        'total_visits': total_visits,
        'stores_visited': len(store_visits),
        'organizations_visited': len(org_visits),
        'favorite_store': favorite_store,
        'favorite_organization': favorite_org,
        'store_visits': list(store_visits),
        'organization_visits': list(org_visits)
    })


# ✅ PRIDANÉ: Endpoint pre štatistiky podľa username
@api_view(['GET'])
@permission_classes([AllowAny])
def public_visits_by_username(request, username):
    """
    Verejný endpoint pre štatistiky podľa username
    """
    user = get_object_or_404(User, username=username)
    total_visits = Receipt.objects.filter(user=user).count()
    
    return Response({
        'user_id': user.id,
        'username': user.username,
        'total_store_visits': total_visits
    })


# ✅ PRIDANÉ: Jednoduchý endpoint pre testovanie
@api_view(['GET'])
@permission_classes([AllowAny])
def public_visit_test(request):
    """
    Jednoduchý testovací endpoint
    """
    return Response({
        'message': 'API je funkčné!',
        'endpoints': [
            '/api/core/public/visits/user/1/total/',
            '/api/core/public/visits/user/1/breakdown/',
            '/api/core/public/visits/user/1/statistics/',
            '/api/core/public/visits/username/<username>/'
        ]
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def public_all_receipts_with_items(request, user_id):
    """
    Verejný endpoint pre zoznam všetkých účteniek so všetkými položkami
    """
    user = get_object_or_404(User, id=user_id)
    
    # Získanie všetkých účteniek používateľa so všetkými potrebnými údajmi
    receipts = Receipt.objects.filter(user=user)\
        .select_related('organization', 'store_unit')\
        .prefetch_related('items__product')\
        .order_by('-issue_date')
    
    receipt_list = []
    
    for receipt in receipts:
        receipt_data = {
            'id_bloku': receipt.fs_receipt_id,  # ID bloku/účtenky
            'datum_bloku': receipt.issue_date,  # Dátum vystavenia
            'celkova_suma': float(receipt.total_price) if receipt.total_price else 0,  # Celková suma
            'organizacia': {
                'nazov': receipt.organization.name if receipt.organization else "Neznáma organizácia",
                'ico': receipt.organization.ico if receipt.organization else None,
            },
            'pobocka': {
                'nazov': receipt.store_unit.name if receipt.store_unit else "Neznáma pobočka",
                'adresa': f"{receipt.store_unit.street_name or ''} {receipt.store_unit.building_number or ''}".strip() if receipt.store_unit else "",
                'mesto': receipt.store_unit.municipality if receipt.store_unit else "",
            },
            'polozky': []  # Zoznam položiek na účtenke
        }
        
        # Pridanie všetkých položiek z účtenky
        for item in receipt.items.all():
            item_data = {
                'nazov_produktu': item.product.name,
                'ai_nazov': item.ai_name_without_brand,
                'mnozstvo': float(item.quantity),
                'jednotkova_cena': float(item.unit_price),
                'celkova_cena_polozky': float(item.total_price),
                'znacka': item.ai_brand,
                'kategoria': item.ai_category
            }
            receipt_data['polozky'].append(item_data)
        
        receipt_list.append(receipt_data)
    
    return Response({
        'user_id': user.id,
        'username': user.username,
        'pocet_ucetniok': len(receipt_list),
        'ucetnicky': receipt_list
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def public_all_products_with_categories(request):
    """
    Verejný endpoint pre zoznam všetkých produktov s kategóriami
    """
    # Získanie všetkých produktov s kategóriami
    products = Product.objects.all()\
        .order_by('name')
    
    product_list = []
    
    for product in products:
        product_data = {
            'id_produktu': product.product_id,
            'nazov_produktu': product.name,
            'povodny_nazov': product.original_name,
            'znacka': product.brand,
            'normalna_kategoria': product.category,  # Normálna kategória
            'ai_kategoria': product.ai_category,  # AI kategória
            'ai_nazov': product.ai_name,  # AI názov
            'ai_nazov_anglicky': product.ai_name_english  # AI názov v angličtine
        }
        product_list.append(product_data)
    
    return Response({
        'pocet_produktov': len(product_list),
        'produkty': product_list
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def public_products_by_category(request, category_type):
    """
    Verejný endpoint pre produkty zoradené podľa kategórie
    category_type: 'normal' pre normálnu kategóriu, 'ai' pre AI kategóriu
    """
    if category_type == 'normal':
        # Produkty zoskupené podľa normálnej kategórie
        products_by_category = Product.objects\
            .exclude(category__isnull=True)\
            .exclude(category='')\
            .values('category')\
            .annotate(pocet_produktov=Count('product_id'))\
            .order_by('-pocet_produktov')
        
        category_list = []
        for category in products_by_category:
            # Produkty v danej kategórii
            products_in_category = Product.objects\
                .filter(category=category['category'])\
                .values('product_id', 'name', 'brand', 'ai_category')
            
            category_list.append({
                'kategoria': category['category'],
                'pocet_produktov': category['pocet_produktov'],
                'produkty': list(products_in_category)
            })
        
        return Response({
            'typ_kategorie': 'normálna_kategoria',
            'pocet_kategorii': len(category_list),
            'kategorie': category_list
        })
    
    elif category_type == 'ai':
        # Produkty zoskupené podľa AI kategórie
        products_by_category = Product.objects\
            .exclude(ai_category__isnull=True)\
            .exclude(ai_category='')\
            .values('ai_category')\
            .annotate(pocet_produktov=Count('product_id'))\
            .order_by('-pocet_produktov')
        
        category_list = []
        for category in products_by_category:
            # Produkty v danej AI kategórii
            products_in_category = Product.objects\
                .filter(ai_category=category['ai_category'])\
                .values('product_id', 'name', 'brand', 'category')
            
            category_list.append({
                'ai_kategoria': category['ai_category'],
                'pocet_produktov': category['pocet_produktov'],
                'produkty': list(products_in_category)
            })
        
        return Response({
            'typ_kategorie': 'ai_kategoria',
            'pocet_kategorii': len(category_list),
            'kategorie': category_list
        })
    
    else:
        return Response({
            'error': 'Neplatný typ kategórie. Použite "normal" alebo "ai".'
        }, status=400)


@api_view(['GET'])
@permission_classes([AllowAny])
def public_product_categories_overview(request):
    """
    Verejný endpoint pre prehľad kategórií
    """
    # Štatistiky pre normálne kategórie
    normal_categories = Product.objects\
        .exclude(category__isnull=True)\
        .exclude(category='')\
        .values('category')\
        .annotate(pocet_produktov=Count('product_id'))\
        .order_by('-pocet_produktov')
    
    # Štatistiky pre AI kategórie
    ai_categories = Product.objects\
        .exclude(ai_category__isnull=True)\
        .exclude(ai_category='')\
        .values('ai_category')\
        .annotate(pocet_produktov=Count('product_id'))\
        .order_by('-pocet_produktov')
    
    # Produkty bez kategórie
    products_without_normal_category = Product.objects\
        .filter(category__isnull=True) | Product.objects.filter(category='')
    products_without_ai_category = Product.objects\
        .filter(ai_category__isnull=True) | Product.objects.filter(ai_category='')
    
    return Response({
        'prehlad_kategorii': {
            'normalne_kategorie': {
                'pocet_kategorii': len(normal_categories),
                'celkovy_pocet_produktov_s_kategoriou': sum(cat['pocet_produktov'] for cat in normal_categories),
                'pocet_produktov_bez_kategorie': products_without_normal_category.count(),
                'top_kategorie': list(normal_categories[:10])  # Top 10 kategórií
            },
            'ai_kategorie': {
                'pocet_kategorii': len(ai_categories),
                'celkovy_pocet_produktov_s_kategoriou': sum(cat['pocet_produktov'] for cat in ai_categories),
                'pocet_produktov_bez_kategorie': products_without_ai_category.count(),
                'top_kategorie': list(ai_categories[:10])  # Top 10 AI kategórií
            }
        }
    })