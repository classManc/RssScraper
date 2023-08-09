from django.shortcuts import render
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework import generics,status
from rest_framework.response import Response


# Create your views here.
class CreateUser(generics.CreateAPIView):
    serializer_class = UserSerializer



class UserLogin(generics.GenericAPIView):
    serializer_class = UserSerializer
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )




