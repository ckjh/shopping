from django.db import models
from admin01.models import Base
from user.models import Client


# Create your models here.

class Orders(models.Model):
    order_sn = models.CharField(max_length=100, unique=True, )  # 订单号
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255, default='')
    status = models.IntegerField(default=0)  # 状态 :  未支付,已支付,支付失败,已评价
    pay_type = models.IntegerField(default=0)  # 支付方式
    code = models.CharField(max_length=250, default='')  # 流水号
    create_time = models.DateField(auto_now_add=True, blank=True)
    update_time = models.DateField(auto_now=True, blank=True)

    class Meta():
        db_table = 'orders'


class OrderDetails(models.Model):
    order_sn = models.ForeignKey(Orders, to_field='order_sn', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    goods_id = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    count = models.IntegerField(default=0)
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    pic = models.CharField(max_length=255)
    is_comment = models.IntegerField(default=0)

    class Meta():
        db_table = 'order_detail'
