# Generated by Django 2.2.2 on 2019-09-05 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20190903_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='goods_id',
            field=models.IntegerField(default=0),
        ),
    ]
