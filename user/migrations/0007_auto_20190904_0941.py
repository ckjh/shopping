# Generated by Django 2.2.2 on 2019-09-04 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20190829_0910'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('code', models.CharField(default='', max_length=50)),
                ('name', models.CharField(max_length=250)),
                ('parent_id', models.IntegerField()),
                ('first_letter', models.CharField(max_length=50)),
                ('level', models.IntegerField()),
            ],
            options={
                'db_table': 'city',
            },
        ),
        migrations.DeleteModel(
            name='UserToken',
        ),
    ]
