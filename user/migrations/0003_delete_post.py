# Generated by Django 4.1.6 on 2023-02-10 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_postlike'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]
