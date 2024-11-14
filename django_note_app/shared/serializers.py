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
        fields = [
            'id',
            'note',
            'note_title',
            'note_content',
            'shared',
            'shared_with_username',
            'can_view',
            'can_edit',
            'shared_at',
            "owner",
        ]
        read_only_fields = ['note_title', 'shared_with_username', 'shared_at']
