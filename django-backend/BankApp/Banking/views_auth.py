from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Sú potrebné prihlasovacie údaje."}, status=400)

    try:
        validate_password(password)
    except ValidationError as e:
        return Response({"error": e.messages}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Použivateľ s týmto menom už existuje."}, status=400)

    user = User.objects.create_user(username=username, password=password)
    return Response({"message": f"Používateľ '{user.username}' bol vytvorený."}, status=201)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Sú potrebné prihlasovacie údaje."}, status=400)

    user = authenticate(username=username, password=password)
    if user is not None:
        return Response({"message": f"Vitajte, {user.username}!"}, status=200)
    else:
        return Response({"error": "Neplatné údaje."}, status=401)