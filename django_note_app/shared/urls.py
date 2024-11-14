# shared/urls.py
from django.urls import path
from .views import SharedViewSet

shared_list = SharedViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

shared_detail = SharedViewSet.as_view({
    'get': 'retrieve',
    'put': 'update'
})

urlpatterns = [
    path('shared/', shared_list, name='shared-list'),
    path('shared/<int:pk>/', shared_detail, name='shared-detail'),
]
