from django.db import models
from admin01.models import Base

# Create your models here.


from django.contrib.auth.models import AbstractUser


class Client(Base, AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=50)
    pic = models.CharField(max_length=255, default='')
    signature = models.CharField(max_length=255, default='')
    is_valid = models.IntegerField(default=0)
    token = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'client'


class City(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=250)
    name = models.CharField(max_length=50)
    parent_id = models.IntegerField()
    first_letter = models.CharField(max_length=30)
    level = models.IntegerField()

    class Meta:
        db_table = 'city'


class Address(models.Model):
    name = models.CharField(max_length=50)
    receiver = models.CharField(max_length=250)
    province_id = models.IntegerField()
    city_id = models.IntegerField()
    district_id = models.IntegerField()
    place = models.CharField(max_length=250)
    mobile = models.CharField(max_length=11)
    tel = models.CharField(max_length=11, default='', null=True)
    email = models.CharField(max_length=50, default='', null=True)
    user_id = models.IntegerField()
    district = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=50, default='')
    province = models.CharField(max_length=50, default='')
    is_default = models.IntegerField(default=0)

    class Meta:
        db_table = 'address'


