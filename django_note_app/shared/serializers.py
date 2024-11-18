# shared/serializers.py
from rest_framework import serializers
from .models import Shared

class SharedSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source="note.title")
    content = serializers.ReadOnlyField(source="note.content")
    type = serializers.ReadOnlyField(source="note.type")
    color = serializers.ReadOnlyField(source="note.color")
    shared_with_username = serializers.ReadOnlyField(source="shared.fullname")
    owner = serializers.ReadOnlyField(source="note.user_id")
    class Meta:
        model = Shared
        fields = '__all__'
        
