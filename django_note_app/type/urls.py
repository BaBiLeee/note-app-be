# note/urls.py
from django.urls import path
from .views import view_type

urlpatterns = [
    path('type/', view_type, name='type'),
]
