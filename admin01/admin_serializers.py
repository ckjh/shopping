from rest_framework import serializers
from admin01 import models
from django.contrib.auth.hashers import make_password, check_password


class CateSerializersModel01(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    def get_parent(self, row):
        if row.pid > 0:
            c = models.Cate.objects.get(id=row.pid)
            name = c.name
        else:
            name = ''
        return name

    """
    分类序列化
    """

    class Meta:
        model = models.Cate
        fields = ('id', 'name', 'parent')


class CateSerializersModel(serializers.ModelSerializer):
    class Meta:
        model = models.Cate
        fields = '__all__'


class CateSerializers(serializers.Serializer):
    """
    分类反序列化,
    """
    name = serializers.CharField()
    pid = serializers.IntegerField()
    type = serializers.IntegerField()
    top_id = serializers.IntegerField()
    is_recommend = serializers.IntegerField()
    pic = serializers.CharField(default='')

    def create(self, data):
        cate = models.Cate.objects.create(**data)
        return cate

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.pid = validated_data['pid']
        instance.type = validated_data['type']
        instance.top_id = validated_data['top_id']
        instance.is_recommend = validated_data['is_recommend']
        instance.pic = validated_data['pic']
        instance.save()
        return instance


class TagSerializersModel(serializers.ModelSerializer):
    cate = serializers.CharField(source='cid.name')

    class Meta:
        model = models.Tags
        fields = '__all__'


class TagSerializers(serializers.Serializer):
    """
    标签的反序列化类
    """
    name = serializers.CharField()
    cid = serializers.IntegerField()
    is_recommend = serializers.IntegerField()

    def create(self, data):
        cid = data['cid']
        cate = models.Cate.objects.get(id=cid)
        tags = models.Tags.objects.create(name=data['name'], is_recommend=data['is_recommend'], cid=cate)
        return tags

    def update(self, instance, validated_data):
        cid = validated_data['cid']
        cate = models.Cate.objects.get(id=cid)
        instance.name = validated_data['name']
        instance.cid = cate
        instance.is_recommend = validated_data['is_recommend']
        instance.save()
        return instance

    # def update(self, instance, validated_data):
    #     instance.name=m


class NewsSerializersModel(serializers.ModelSerializer):
    class Meta:
        model = models.News
        fields = '__all__'


class NewsSerializers(serializers.Serializer):
    """
    分类反序列化,
    """
    title = serializers.CharField()
    content = serializers.CharField()
    is_recommend = serializers.IntegerField()

    def create(self, data):
        news = models.News.objects.create(**data)
        return news

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.content = validated_data['content']
        instance.is_recommend = validated_data['is_recommend']
        instance.save()
        return instance


class BannerSerializersModel(serializers.ModelSerializer):
    class Meta:
        model = models.Banner
        fields = '__all__'


class BannerSerializers(serializers.Serializer):
    """
    分类反序列化,
    """
    name = serializers.CharField()
    is_show = serializers.IntegerField()
    sort = serializers.IntegerField()
    type = serializers.IntegerField()

    def create(self, data):
        banner = models.Banner.objects.create(**data)
        return banner

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.is_show = validated_data['is_show']
        instance.sort = validated_data['sort']
        instance.type = validated_data['type']
        instance.save()
        return instance


class GoodsSerializersModel(serializers.ModelSerializer):
    price = serializers.FloatField()

    class Meta:
        model = models.Goods
        fields = '__all__'


class GoodsSerializers(serializers.Serializer):
    """
    分类反序列化,
    """
    name = serializers.CharField()
    cid = serializers.IntegerField()
    tid = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=99999, decimal_places=2, default=99999)
    stock = serializers.IntegerField()
    lock_stock = serializers.IntegerField()
    is_recommend = serializers.IntegerField()
    desc = serializers.CharField()
    pic = serializers.CharField(default='', allow_null=True)
    top_id = serializers.IntegerField()

    def create(self, data):
        cate = models.Cate.objects.get(id=int(data['cid']))
        tag = models.Tags.objects.get(id=int(data['tid']))
        goods = models.Goods.objects.create(
            name=data['name'],
            cid=cate,
            tid=tag,
            desc=data['desc'],
            price=data['price'],
            stock=data['stock'],
            lock_stock=data['lock_stock'],
            pic=data['pic'],
            is_recommend=data['is_recommend'],
            top_id=data['top_id']
        )
        return goods

    def update(self, instance, validated_data):
        cate = models.Cate.objects.get(id=int(validated_data['cid']))
        tag = models.Tags.objects.get(id=int(validated_data['tid']))
        pic = validated_data['pic']
        instance.pic = pic
        instance.name = validated_data['name']
        instance.cid = cate
        instance.tid = tag
        instance.desc = validated_data['desc']
        instance.price = validated_data['price']
        instance.stock = validated_data['stock']
        instance.is_recommend = validated_data['is_recommend']
        instance.top_id = validated_data['top_id']
        instance.save()
        return instance
    # def update(self, instance, validated_data):
    #     instance.name = validated_data['name']
    #     instance.is_show = validated_data['is_show']
    #     instance.sort = validated_data['sort']
    #     instance.type = validated_data['type']
    #     instance.save()
    #     return instance


class ResourceSerializersModel(serializers.ModelSerializer):
    class Meta:
        model = models.Resource
        fields = '__all__'


class ConnSerializersModel(serializers.ModelSerializer):
    # parent = serializers.SerializerMethodField()
    rid = serializers.IntegerField(source='role_id.id')
    name = serializers.CharField(source='role_id.name')
    resource = serializers.CharField(source='resource_id.name')
    status = serializers.CharField(source='resource_id.status')

    class Meta:
        model = models.Connect
        # fields = ('id', 'name', 'parent', 'status')
        fields = "__all__"


class RoleSerializersModel(serializers.ModelSerializer):
    # parent = serializers.SerializerMethodField()

    class Meta:
        model = models.Role
        # fields = ('id', 'name', 'parent', 'status')
        fields = "__all__"


class UserSerializersModel(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


class ResourceSerializers(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.CharField()
    status = serializers.IntegerField()

    # def create(self, validated_data):
    #     resource = models.Resource.objects.create(**validated_data)
    #     return resource

    def create(self, data):
        banner = models.Resource.objects.create(**data)
        return banner

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.status = validated_data['status']
        instance.url = validated_data['url']
        instance.save()

        return instance


class RoleSerializers(serializers.Serializer):
    name = serializers.CharField()
    status = serializers.IntegerField()

    def create(self, data):
        banner = models.Role.objects.create(**data)
        return banner

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.status = validated_data['status']
        instance.save()
        return instance


class UserSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    role_id = serializers.IntegerField()
    is_admin = serializers.IntegerField()

    def create(self, data):
        role = models.Role.objects.get(id=int(data['role_id']))
        user = models.User.objects.create(role_id=role,
                                          username=data['username'],
                                          password=make_password(data['password']),
                                          is_admin=data['is_admin'])

        return user

    def update(self, instance, validated_data):
        role = models.Role.objects.get(id=int(validated_data['role_id']))
        instance.role_id = role
        instance.username = validated_data['username']
        instance.is_admin = validated_data['is_admin']
        if instance.password != validated_data['password']:
            instance.password = make_password(validated_data['password'])
        instance.save()
        return instance


class BannerSerializers(serializers.Serializer):
    name = serializers.CharField()

    def create(self, data):
        banner = models.Banner.objects.create(**data)
        return banner

    def update(self, instance, validated_data):
        pass
        instance.save()
        return instance
