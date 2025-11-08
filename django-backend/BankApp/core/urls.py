from django.urls import path
from . import views
from .views import ProductListView
from .views import current_user

urlpatterns = [
    path('chat/start/', views.start_chat, name='start_chat'),
    path('chat/<int:session_id>/send/', views.send_message, name='send_message'),
    path('chat/<int:session_id>/history/', views.get_chat_history, name='chat_history'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('receipt/<str:fs_receipt_id>/', views.receipt_detail_api, name='receipt-detail'),
    path('receipt/<str:fs_receipt_id>/page/', views.receipt_detail_page, name='receipt-detail-page'),
    
    # Existujúce endpoints pre štatistiky
    path('public/visits/user/<int:user_id>/total/', views.public_total_store_visits, name='public-total-visits'),
    path('public/visits/user/<int:user_id>/breakdown/', views.public_store_visits_breakdown, name='public-visit-breakdown'),
    path('public/visits/user/<int:user_id>/statistics/', views.public_user_visit_statistics, name='public-visit-statistics'),
    path('public/visits/username/<str:username>/', views.public_visits_by_username, name='public-visits-by-username'),
    path('public/visits/test/', views.public_visit_test, name='public-visit-test'),
    
    # ✅ NOVÝ endpoint pre všetky účtenky s položkami
    path('public/receipts/user/<int:user_id>/all/', views.public_all_receipts_with_items, name='public-all-receipts'),
    
    # ✅ NOVÉ endpoints pre produkty a kategórie
    path('public/products/all/', views.public_all_products_with_categories, name='public-all-products'),
    path('public/products/category/<str:category_type>/', views.public_products_by_category, name='public-products-by-category'),
    path('public/products/categories/overview/', views.public_product_categories_overview, name='public-products-categories-overview'),

    path('user/', current_user, name='current-user'),
]