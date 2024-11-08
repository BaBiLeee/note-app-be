# Generated by Django 5.1.3 on 2024-11-08 03:14

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.TextField()),
                ('password', models.TextField()),
                ('fullname', models.TextField()),
                ('avatar', models.TextField()),
                ('group', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, size=None)),
                ('permission', models.IntegerField()),
                ('note', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, size=None)),
                ('admin', models.BooleanField()),
            ],
        ),
    ]
