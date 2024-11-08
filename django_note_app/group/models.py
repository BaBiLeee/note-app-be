from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Group(models.Model):
    user = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'group'