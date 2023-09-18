from django.urls import path, include
from .views import CreateUser, UserLogin,ForgotPass,ResetPassword,ResetAuthUserPassword

urlpatterns = [
    path('', CreateUser.as_view(), name='list_user'),
    path('login', UserLogin.as_view(), name='user_login'),
    path('forgotpassword', ForgotPass.as_view(), name='forgot_password'),
    path('reset-password', ResetPassword.as_view(), name='reset_password'),
    path('reset-password-authuser', ResetAuthUserPassword.as_view(), name='reset_auth_user_password')
]

