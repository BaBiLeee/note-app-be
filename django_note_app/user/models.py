from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class User(models.Model):
    username = models.TextField()
    password = models.TextField()
    fullname = models.TextField(blank=True, null=True)
    avatar = models.TextField(blank=True, null=True)
    group = models.TextField(blank=True, null=True)  # This field type is a guess.
    permission = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)  # This field type is a guess.
    admin = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
