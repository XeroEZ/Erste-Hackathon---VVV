from django.urls import path
from .views import chat_response, chat_history

urlpatterns = [
    path('response/', chat_response, name='chat-response'),
    path('history/', chat_history, name='chat-history'),
]
