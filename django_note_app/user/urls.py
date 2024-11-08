# note/urls.py
from django.urls import path
from .views import view_user, UserRegistrationView, LoginAPI

urlpatterns = [
    path('user/', view_user, name='user'),
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('login/', LoginAPI.as_view(), name='user_login'),
]
