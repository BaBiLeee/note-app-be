from django.db import models
from user.models import User
from note.models import Note
# Create your models here.

class SharedNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  
    permission = models.IntegerField()  
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.TextField(blank=True, null=True)  
    
    def __str__(self):
        return f"{self.user.fullname} - {self.note.title} - {self.get_access_level_display()}"

    class Meta:
        # managed = False
        db_table = 'shared_note'
    

