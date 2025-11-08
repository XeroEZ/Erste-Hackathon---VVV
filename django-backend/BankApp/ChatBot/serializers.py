from rest_framework import serializers

class ChatRequestSerializer(serializers.Serializer):
    question = serializers.CharField(
        max_length=1000,  # nastav podľa potreby
        help_text="Zadajte otázku, na ktorú chce Gemini odpovedať."
    )
