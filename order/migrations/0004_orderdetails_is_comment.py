# Generated by Django 2.2.2 on 2019-09-06 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_orderdetails_goods_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='is_comment',
            field=models.IntegerField(default=0),
        ),
    ]
