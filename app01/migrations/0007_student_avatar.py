# Generated by Django 2.1 on 2020-02-07 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_auto_20200205_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='avatar',
            field=models.ImageField(default='avatar.jpg', max_length='100', upload_to='./static/avatar/', verbose_name='照片'),
        ),
    ]
