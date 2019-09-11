from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
class Base(object):
    create_time = models.DateField(auto_now_add=True)
    update_time = models.DateField(auto_now=True)

    class Meta():
        abstract = False  # 这个类不生成对象


# 考虑后续的扩展
# 分类

class Cate(models.Model, Base):
    name = models.CharField(max_length=50, unique=True)
    pid = models.IntegerField(default=0, null=False)  # 上级分类ID
    type = models.IntegerField(default=1)  # 标识分类等级
    top_id = models.IntegerField(default=0)  # 顶级分类ID
    is_recommend = models.IntegerField(default=1)  # 是否退推荐到首页
    pic = models.CharField(max_length=245, default=0)  # 图片

    class Meta():
        db_table = 'cate'


# 标签表
class Tags(models.Model, Base):
    name = models.CharField(max_length=50, unique=True)
    cid = models.ForeignKey(Cate, to_field='id', on_delete=models.CASCADE)  # 上级分类ID,to_field默认为主键,订单的ID
    # 是订单号
    is_recommend = models.IntegerField(default=1)  # 是否退推荐到首页

    class Meta():
        db_table = 'tag'


# 焦点图表
class Banner(Base, models.Model):
    name = models.CharField(max_length=250, unique=True)
    is_show = models.IntegerField(default=1)  # 是否退推荐到首页
    sort = models.IntegerField(default=1)  # 图的排序
    type = models.IntegerField(default=0)  # 焦点图

    class Meta():
        db_table = 'banner'


# # 新闻表
class News(Base, models.Model):
    title = models.CharField(max_length=200, default='')
    is_recommend = models.IntegerField(default=0)  # 是否退推荐到首页
    content = models.TextField()

    class Meta():
        db_table = 'news'


#     status = models.IntegerField(default=0)


#     reason = models.CharField(max_length=255)
#
#
# # 用户表
#
# class User(Base, models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     phone = models.CharField(max_length=11)
#     email = models.CharField(max_length=50)
#     image = models.CharField(max_length=255, default='')
#     # 签名...
#     is_alive = models.IntegerField(default=0)


#
# # 产品表(没写完)
# 加一个评价数
# 高频页面,不是每次都访问数据库
# 单张图片,用一张表
# 多张图用,一个图片表,(事务)

class Goods(Base, models.Model):
    '''评论数,销量需要依赖其他表'''
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=255, default='')
    price = models.DecimalField(max_digits=64, decimal_places=2, default=999999)
    pic = models.CharField(max_length=250, default='', null=False)
    stock = models.IntegerField(default=0, null=False)  # 库存
    # 锁定库存
    lock_stock = models.IntegerField(default=0, null=False)
    is_recommend = models.IntegerField(default=1)  # 是否退推荐到首页
    cid = models.ForeignKey('Cate', on_delete=models.CASCADE, default=0)
    tid = models.ForeignKey('Tags', on_delete=models.CASCADE, default=0)
    top_id = models.IntegerField(default=0)  # 顶级分类
    comment_time = models.IntegerField(default=0)  # 评论数
    sales = models.IntegerField(default=0)  # 销量

    class Meta():
        db_table = 'goods'


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    status = models.IntegerField(default=1)

    class Meta():
        db_table = 'role'


class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    is_admin = models.IntegerField(default=0)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta():
        db_table = 'user'


class Resource(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=255, default='')
    status = models.IntegerField(default=0)

    class Meta():
        db_table = 'resource'


class Connect(models.Model):
    """关系表"""
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    resource_id = models.ForeignKey(Resource, on_delete=models.CASCADE)

    class Meta():
        db_table = 'connect'
