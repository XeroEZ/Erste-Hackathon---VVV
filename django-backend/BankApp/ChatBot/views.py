from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ChatRequestSerializer
from . import geminiKey
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

# Your existing Gemini function
@permission_classes([AllowAny])
def OtazkaNaGeminiBasic(otazka: str) -> str:
    try:
        client = geminiKey.ClientApi()
        prompt_text = ({otazka})



        config = geminiKey.types.GenerateContentConfig(
            temperature=0.0

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text,
            config=config,
        )
        return response.text.strip()

    except Exception as e:
        return f"Nastala chyba pri volaní AI: {e}"

# API endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def chat_response(request):
    serializer = ChatRequestSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.validated_data['question']
        answer = OtazkaNaGeminiBasic(question)
        return Response({
            "request": question,
            "response": answer
        })
    return Response(serializer.errors, status=400)
