from django.db import models

# Create your models here.

class Type(models.Model):
    type = models.TextField()

    class Meta:
        managed = False
        db_table = 'type'