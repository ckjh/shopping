# Generated by Django 2.2.2 on 2019-09-06 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_comment_is_anonymity'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='comment',
            table='commit',
        ),
    ]