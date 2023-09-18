from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate
from .serializers import UserSerializer, ForgotPassSerializer,ResetPassSerializer,UserLoginSerializer,ChangePasswordSerializer
from rest_framework.authtoken.models import Token
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
import uuid
from .models import ResetToken
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import timedelta
from django.utils import timezone
# Create your views here.


class CreateUser(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserLogin(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    
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

class ForgotPass(generics.GenericAPIView):
    serializer_class = ForgotPassSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')

            try:
                user = User.objects.get(email=email)

            except User.DoesNotExist:
                return Response(
                    {"error": "No user with this email exists"},
                    status=status.HTTP_404_NOT_FOUND
                )
            reset_token = uuid.uuid4().hex
            # expiration_duration = timedelta(hours=24)  # Adjust as needed
            # expires_at = timezone.now() + expiration_duration
            user_token = ResetToken.objects.create(token=reset_token, user=user)
            reset_link = f" http://127.0.0.1:8000/reset-password"

            subject = "Password Reset Instructions"
            message = f"Click the following link to reset your password: {reset_link} and use this {user_token} to confirm that you initiated the process"
            recipient_list = [email]
            from_email = 'josephajakaye924@gmail.com'

            send_mail(subject, message,from_email=from_email, recipient_list=recipient_list, fail_silently=False)

            return Response(
                {"message": "Password reset instructions have been sent to your email"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPassSerializer

    
    def post(self,request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            new_password = serializer.validated_data.get('password')
            token = serializer.validated_data.get('token')
            
        try:
            token = ResetToken.objects.get(token=token)
            user = token.user

        except ResetToken.DoesNotExist:
            return JsonResponse({"error": "Invalid Token"}, status=status.HTTP_404_NOT_FOUND)
        
        current_datetime = timezone.now()
        if current_datetime >= token.expires_at:
            return Response(
                {"message": "Token expired"},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            user.set_password(new_password)
            user.save()
            return Response(
                {"message": "Password reset successfull"},
                status=status.HTTP_200_OK
            )
        

class ResetAuthUserPassword(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                old_password = serializer.validated_data.get('old_password')
                new_password = serializer.validated_data.get('new_password')
                user = User.objects.get(username = request.user.username)
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    return Response({'message': 'Password successfully changed'}, status=status.HTTP_200_OK)
                return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)







