# Generated by Django 2.2.2 on 2019-09-03 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='is_checked',
            field=models.IntegerField(default=0),
        ),
    ]