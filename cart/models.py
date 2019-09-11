from django.db import models


# Create your models here.

class Cart(models.Model):
    user_id = models.IntegerField()
    goods_id = models.IntegerField()
    count = models.IntegerField()
    goods_name = models.CharField(max_length=50)
    pic = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_checked = models.IntegerField(default=0)

    class Meta():
        db_table = 'cart'
