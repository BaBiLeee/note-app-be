from django.urls import path
from . import views

urlpatterns = [
    path('shared-note/<int:note_id>/', views.shared_note_detail, name='shared_note_detail'),
]
