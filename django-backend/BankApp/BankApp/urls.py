# BankApp/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD

    # JWT autentifikácia
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API aplikácie
    path('api/banking/', include('Banking.urls')),
    path('api/core/', include('core.urls')),
]
=======
    path('api/', include('Banking.urls'))
]
>>>>>>> fd9e7b8f571011a4d79ce3b6ece6b9a257f50c66
