# Generated by Django 2.2.2 on 2019-09-06 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_anonymity',
            field=models.IntegerField(default=0),
        ),
    ]
