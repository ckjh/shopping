# Generated by Django 2.2.2 on 2019-09-04 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20190904_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='address',
            name='district',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='address',
            name='province',
            field=models.CharField(default='', max_length=50),
        ),
    ]
