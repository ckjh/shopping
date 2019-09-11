import redis
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from cart.models import *
from admin01.models import Goods
from utils.redis_pool import POOL


class CartSerializers(serializers.Serializer):
    user_id = serializers.IntegerField()
    goods_id = serializers.IntegerField()
    count = serializers.IntegerField()
    goods_name = serializers.CharField()
    pic = serializers.CharField()
    price = serializers.DecimalField(max_digits=7, decimal_places=2)

    def create(self, data):
        user = Cart.objects.create(**data)
        user.save()
        return user


class CartSerializersModel(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request):
        ret = {}
        # print(data)
        conn = redis.Redis(connection_pool=POOL)
        is_checked = request.GET.get('is_checked')
        id = int(request.GET.get('user_id'))
        cList = []
        if is_checked:
            cartList = conn.hgetall('cart' + str(id))
            for cart in cartList:
                cDict = json.loads(cartList[cart].decode())
                if cDict['is_checked'] == '1':
                    cList.append(cDict)
        else:
            cartList = conn.hgetall('cart' + str(id))
            for cart in cartList:
                cList.append(json.loads(cartList[cart].decode()))
        ret['cartList'] = cList
        ret['code'] = '200'
        ret['message'] = 'OK'
        print(ret)
        return Response(ret)


from django_redis import get_redis_connection
import json


class AddCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):
        # 添加购物车用的data: < QueryDict: {'count': ['4'], 'goods_id': ['28'], 'user_id': ['34']} >
        # 最终存入的数据
        # <QueryDict: {'count': ['4'], 'goods_id': ['28'], 'user_id': ['34'], 'pic': ['http://127.0.0.1:8000/static/iwI_nK6rlfHW3LMRidGUSg.jpg'], 'price': [Decimal('5432.00')], 'goods_name': ['甲3']}>
        ret = {}
        data = request.data.copy()
        # 判断是否以存在,
        conn = redis.Redis(connection_pool=POOL)
        # conn.set(key, value)
        try:
            cart = conn.hget('cart' + data['user_id'], data['goods_id']).decode('utf-8')
            # 若存在,则数量加
            cart = json.loads(cart)
            oldCount = cart['count']
            cart['count'] = str(int(oldCount) + int(data['count']))
            conn.hset('cart' + str(data['user_id']), data['goods_id'], json.dumps(cart))
            ret['code'] = 200
            ret['message'] = '添加成功'
        except Exception as e:
            # 创建购物车
            goods = Goods.objects.get(id=data['goods_id'])
            cartDict = {}
            cartDict['pic'] = str(goods.pic)
            cartDict['price'] = str(goods.price)
            cartDict['goods_name'] = str(goods.name)
            cartDict['is_checked'] = str(0)
            cartDict['count'] = str(data['count'])
            cartDict['goods_id'] = str(data['goods_id'])
            cartDict['user_id'] = str(data['user_id'])
            conn.hset('cart' + str(data['user_id']), str(data['goods_id']), json.dumps(cartDict))
            goods = conn.hget('cart' + data['user_id'], data['goods_id'])
            ret['code'] = 200
            ret['message'] = '添加成功'
        return Response(ret)


class DeleteCartAPIVIew(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):
        ret = {}
        conn = redis.Redis(connection_pool=POOL)
        data = request.data
        conn.hdel('cart' + data['user_id'], data['goods_id'])
        ret['code'] = 200
        ret['message'] = '成功删除'
        return Response(ret)


class AddReduceCountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):
        conn = redis.Redis(connection_pool=POOL)
        data = request.data
        ret = {}
        cart = conn.hget('cart' + data['user_id'], data['goods_id']).decode('utf-8')
        cart = json.loads(cart)
        # 修改数量
        goods = Goods.objects.get(id=int(data['goods_id']))
        if int(data['count']) < goods.stock:
            cart['count'] = str(data['count'])
            conn.hset('cart' + str(data['user_id']), data['goods_id'], json.dumps(cart))
            ret['code'] = 200
            ret['message'] = 'ok'
        else:
            ret['code'] = 613
            ret['message'] = '已达上限'
        return Response(ret)


class SubmitCartAPIView(APIView):
    """
    提交购物车
    """

    def post(self, request):
        ret = {}
        try:
            conn = redis.Redis(connection_pool=POOL)
            data = request.data
            goods_id = str(data['id']).split(',')
            for i in goods_id:
                cart = conn.hget('cart' + data['user_id'], str(i)).decode('utf-8')
                cart = json.loads(cart)
                cart['is_checked'] = '1'
                conn.hset('cart' + str(data['user_id']), str(i), json.dumps(cart))
                ret['code'] = 200
                ret['message'] = '成功'
        except:
            ret['code'] = 601
            ret['message'] = '失败'
        return Response(ret)
