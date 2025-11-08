from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ChatRequestSerializer
from . import geminiKey
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .gemini_main import OtazkaUzivatela
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import SessionAuthentication

from .serializers import ChatRequestSerializer
from ChatBot import geminiKey
from rest_framework.permissions import IsAuthenticated  


from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from .serializers import ChatRequestSerializer
from rest_framework.permissions import AllowAny
from .gemini_main import OtazkaUzivatela
from rest_framework.authentication import SessionAuthentication


# Custom authentication class that skips CSRF
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # Skip CSRF check


# API endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([CsrfExemptSessionAuthentication])
def chat_response(request):
    serializer = ChatRequestSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.validated_data['question']
        answer = OtazkaUzivatela(question)
        return Response({
            "request": question,
            "response": answer
        })
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_history(request):
    user = request.user
    session = ChatSession.objects.filter(user=user).first()

    if not session:
        return Response({"messages": []})

    messages = session.messages.values("sender", "message", "created_at")
    return Response({"session_id": session.id, "messages": list(messages)})