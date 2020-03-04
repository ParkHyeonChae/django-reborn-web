# Generated by Django 3.0.2 on 2020-03-04 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0003_auto_20200305_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='part',
            field=models.CharField(choices=[('회장단', '회장단'), ('개발부', '개발부'), ('학술부', '학술부'), ('운영부', '운영부'), ('홍보부', '홍보부'), ('재정부', '재정부')], max_length=10, verbose_name='부서'),
        ),
    ]
