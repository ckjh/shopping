# Generated by Django 2.2.2 on 2019-09-04 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20190904_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]