# Generated by Django 4.2.6 on 2023-10-30 15:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quora_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_answers', to=settings.AUTH_USER_MODEL),
        ),
    ]
