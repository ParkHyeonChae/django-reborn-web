# Generated by Django 3.0.2 on 2020-02-26 09:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('anonymous', '0007_auto_20200204_0433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anonymouscomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='anonymous.Anonymous', verbose_name='게시글'),
        ),
        migrations.AlterField(
            model_name='anonymouscomment',
            name='writer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='댓글작성자'),
        ),
    ]