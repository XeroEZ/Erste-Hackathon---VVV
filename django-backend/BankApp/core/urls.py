# core/urls.py
from django.urls import path
from . import views
from .views import ProductListView

urlpatterns = [
    path('chat/start/', views.start_chat, name='start_chat'),
    path('chat/<int:session_id>/send/', views.send_message, name='send_message'),
    path('chat/<int:session_id>/history/', views.get_chat_history, name='chat_history'),
    path('products/', ProductListView.as_view(), name='product-list'),
]
