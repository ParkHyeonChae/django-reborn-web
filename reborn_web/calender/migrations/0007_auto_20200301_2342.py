# Generated by Django 3.0.2 on 2020-03-01 14:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('calender', '0006_auto_20200229_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calender',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 1, 20, 12, 0, 949911, tzinfo=utc), verbose_name='수정일'),
        ),
    ]