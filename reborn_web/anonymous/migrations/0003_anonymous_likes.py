# Generated by Django 3.0.2 on 2020-02-01 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anonymous', '0002_auto_20200202_0648'),
    ]

    operations = [
        migrations.AddField(
            model_name='anonymous',
            name='likes',
            field=models.PositiveIntegerField(default=0, verbose_name='추천수'),
        ),
    ]