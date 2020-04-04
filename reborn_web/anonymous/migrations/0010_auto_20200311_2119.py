# Generated by Django 3.0.2 on 2020-03-11 12:19

import anonymous.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anonymous', '0009_auto_20200303_2128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anonymous',
            name='files',
        ),
        migrations.AddField(
            model_name='anonymous',
            name='image_files',
            field=models.ImageField(blank=True, null=True, upload_to=anonymous.models.get_image_path, verbose_name='이미지파일'),
        ),
    ]