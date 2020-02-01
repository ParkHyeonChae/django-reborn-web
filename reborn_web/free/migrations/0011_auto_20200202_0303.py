# Generated by Django 3.0.2 on 2020-02-01 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('free', '0010_auto_20200131_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='free',
            name='category',
            field=models.CharField(choices=[('자유', '자유'), ('질문', '질문'), ('정보', '정보')], default='자유', max_length=18, verbose_name='분류'),
        ),
        migrations.AddField(
            model_name='free',
            name='comments',
            field=models.PositiveIntegerField(null=True, verbose_name='댓글수'),
        ),
        migrations.AddField(
            model_name='free',
            name='upload_files',
            field=models.FileField(blank=True, null=True, upload_to='upload_file/%Y/%m/%d', verbose_name='파일'),
        ),
        migrations.AlterField(
            model_name='free',
            name='files',
            field=models.FileField(blank=True, null=True, upload_to='upload_file/%Y/%m/%d', verbose_name='이미지'),
        ),
    ]
