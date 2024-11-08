# note/urls.py
from django.urls import path
from .views import view_group

urlpatterns = [
    path('group/', view_group, name='group'),
]
