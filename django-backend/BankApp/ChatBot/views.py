from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ChatRequestSerializer
from . import geminiKey
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .gemini_main import OtazkaUzivatela



# API endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
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
