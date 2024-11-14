# shared/models.py
from django.db import models
from user.models import User
from note.models import Note

class Shared(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='shared_notes')
    shared = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_with_user')
    can_view = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shared'
        unique_together = ('note', 'shared')
