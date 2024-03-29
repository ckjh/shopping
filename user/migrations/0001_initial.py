# Generated by Django 2.2.2 on 2019-08-27 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=50)),
                ('pic', models.CharField(default='', max_length=255)),
                ('signator', models.CharField(default='', max_length=255)),
                ('is_valide', models.IntegerField(default=0)),
                ('token', models.CharField(default='', max_length=255)),
            ],
            options={
                'db_table': 'client',
            },
        ),
    ]
