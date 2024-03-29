# Generated by Django 2.2.2 on 2019-09-06 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('goods_id', models.IntegerField()),
                ('content', models.CharField(default='', max_length=250)),
                ('score', models.IntegerField(default=0)),
                ('id_audit', models.IntegerField(default=0)),
                ('pid', models.IntegerField(default=0)),
                ('create_time', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
