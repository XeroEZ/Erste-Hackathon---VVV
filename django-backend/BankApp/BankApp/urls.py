# BankApp/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # JWT autentifikácia
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API aplikácie
    path('api/banking/', include('Banking.urls')),
    path('api/core/', include('core.urls')),
  
    #API chatbot
    path('chat/', include('ChatBot.urls')),
]
