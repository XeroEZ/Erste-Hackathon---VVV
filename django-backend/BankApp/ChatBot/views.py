from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ChatRequestSerializer
from . import geminiKey
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

@permission_classes([AllowAny])
def OtazkaNaGeminiBasic(otazka: str) -> str:
    try:
        client = geminiKey.ClientApi()
        prompt_text = ({otazka})

        # Enable Google Search grounding
        config = geminiKey.types.GenerateContentConfig(
            temperature=0.0,
            grounding=geminiKey.types.GroundingConfig(
                enable_google_search=True,  # <-- This enables grounding
                # Optional: specify max number of search results
                max_search_results=3
            )
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text,
            config=config,
        )
        return response.text.strip()

    except Exception as e:
        return f"Nastala chyba pri volaní AI: {e}"
