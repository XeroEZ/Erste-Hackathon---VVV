from django.urls import path
from .views import chat_response

urlpatterns = [
    path('response/', chat_response, name='chat-response'),
]
