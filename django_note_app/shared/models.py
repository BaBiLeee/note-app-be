# shared/models.py
from django.db import models
from user.models import User
from note.models import Note

class Shared(models.Model):
    VIEW = 1      # Quyền xem
    EDIT = 2      # Quyền sửa
    DELETE = 4    # Quyền xóa
    SHARE = 8     # Quyền chia sẻ

    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='shared_notes')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_with_user')
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_by')
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_user')
    permission = models.IntegerField()
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shared'
        # unique_together = ('note', 'shared')
