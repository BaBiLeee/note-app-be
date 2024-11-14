# note/urls.py
from django.urls import path
from .views import VerifyEmailView, view_user, UserRegistrationView, LoginAPI, user_list

urlpatterns = [
    path('user/', view_user, name='user'),
    path('userList/', user_list, name='userList'),
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('login/', LoginAPI.as_view(), name='user_login'),
    path('verify/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
]
