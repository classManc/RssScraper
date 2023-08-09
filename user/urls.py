from django.urls import path, include
from .views import CreateUser, UserLogin

urlpatterns = [
    path('', CreateUser.as_view(), name='list_user'),
    path('login', UserLogin.as_view(), name='user_login')
]
