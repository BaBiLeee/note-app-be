from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="user.avatar")
    class Meta:
        model = Note
        fields = '__all__'
