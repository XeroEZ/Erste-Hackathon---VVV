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


@csrf_exempt  # 💥 pridaj tento dekorátor
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

