# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Group(models.Model):
    user = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'group'


class Note(models.Model):
    title = models.TextField()
    content = models.TextField()
    type = models.IntegerField()
    create_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'note'


class Type(models.Model):
    type = models.TextField()

    class Meta:
        managed = False
        db_table = 'type'


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
