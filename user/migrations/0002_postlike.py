# Generated by Django 4.1.6 on 2023-02-08 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.BigIntegerField()),
                ('username', models.CharField(max_length=200)),
            ],
        ),
    ]
