# Generated by Django 4.2.2 on 2023-06-14 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0002_video_media_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='duration',
            field=models.IntegerField(default=0),
        ),
    ]