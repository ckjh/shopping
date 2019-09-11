from django.db import models
from user.models import Client


# Create your models here.


class Comment(models.Model):
    user_id = models.IntegerField(default=0)
    goods_id = models.IntegerField()
    content = models.CharField(max_length=250, default='')  # 内容
    score = models.IntegerField(default=0)  # 评分
    id_audit = models.IntegerField(default=0)  # 是否审核
    pid = models.IntegerField(default=0)
    create_time = models.DateField(auto_now_add=True)
    is_anonymity = models.IntegerField(default=0)  # 是否匿名

    class Meta():
        db_table = 'comment'
