from django.db import models
# Create your models here.

class Note(models.Model):
    title = models.TextField()
    content = models.TextField()
    type = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'note'
    

    

    
