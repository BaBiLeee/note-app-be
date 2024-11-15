# shared/serializers.py
from rest_framework import serializers
from .models import Shared

class SharedSerializer(serializers.ModelSerializer):
    note_title = serializers.ReadOnlyField(source="note.title")
    note_content = serializers.ReadOnlyField(source="note.content")
    shared_with_username = serializers.ReadOnlyField(source="shared.fullname")
    owner = serializers.ReadOnlyField(source="note.user_id")
    class Meta:
        model = Shared
        fields = '__all__'
        
