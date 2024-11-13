from django.db import models
from user.models import User
# Create your models here.

class Note(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    type = models.IntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'note'
    


    

    
