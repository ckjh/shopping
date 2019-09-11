import json
import uuid

import redis
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from cart.models import *
from admin01.models import Goods
from order import models
from cart.models import Cart
from admin01.models import Goods
from django.db import transaction
from user.models import Address
from datetime import datetime
from goods.models import Comment
from utils.redis_pool import POOL


class OrderSerializersModel(serializers.ModelSerializer):
    class Meta:
        model = models.OrderDetails
        fields = '__all__'


class TSerializersModel(serializers.ModelSerializer):
    class Meta:
        model = models.Orders
        fields = '__all__'


# Create your views here.

class CreateOrderAPIView(APIView):

    @transaction.atomic
    def post(self, request):
        ret = {}
        data = request.data
        user_id = data['user_id']
        conn = redis.Redis(connection_pool=POOL)
        cartList = conn.hgetall('cart' + str(user_id))
        is_cartList = False
        for cart in cartList:
            theCart = json.loads(cartList[cart].decode())
            print(theCart)
            if json.loads(cartList[cart].decode())['is_checked'] == '1':
                print(json.loads(cartList[cart].decode())['is_checked'], '=============================')
                is_cartList = True

        # 根据 address_id 获取地址
        address_id = data['address_id']
        address = Address.objects.get(id=int(address_id))
        pay_type = data['pay_id']
        # 生成订单号
        order_sn = uuid.uuid1()
        # 计算总价
        tMoney = 0
        sid = transaction.savepoint()
        # 生成订单
        try:
            order = models.Orders.objects.create(order_sn=order_sn,
                                                 user_id=user_id,
                                                 money=tMoney,
                                                 pay_type=pay_type,
                                                 address=address.name)

            # 判断商品库存
            print(is_cartList)
            if not is_cartList:
                count = int(data['count'])
                goods_id = data['goods_id']
                goods = Goods.objects.get(id=goods_id)
                if count > goods.stock - goods.lock_stock:
                    transaction.savepoint_rollback(sid)
                    ret['code'] = 606
                    ret['message'] = '库存不足'
                    return Response(ret)
                else:
                    orderDetail = models.OrderDetails.objects.create(order_sn=order,
                                                                     goods_id=goods.id,
                                                                     name=goods.name,
                                                                     price=goods.price,
                                                                     count=count,
                                                                     user_id=user_id,
                                                                     pic=goods.pic)
                    tMoney += goods.price * count
                    goods.lock_stock += count
                    goods.save()
            else:
                for cart in cartList:
                    theCart = json.loads(cartList[cart].decode())
                    if theCart['is_checked'] == '1':

                        goods = Goods.objects.get(id=int(theCart['goods_id']))
                        if int(theCart['count']) > goods.stock - goods.lock_stock:
                            transaction.savepoint_rollback(sid)
                            ret['code'] = 606
                            ret['message'] = '库存不足'
                            return Response(ret)
                        else:
                            print('库存充足')
                            orderDetail = models.OrderDetails.objects.create(order_sn=order,
                                                                             goods_id=goods.id,
                                                                             name=goods.name,
                                                                             price=goods.price,
                                                                             count=int(theCart['count']),
                                                                             user_id=user_id,
                                                                             pic=goods.pic)
                            tMoney += goods.price * int(theCart['count'])
                        goods.lock_stock += int(theCart['count'])
                        goods.save()
            order.money = tMoney
            order.save()
            # 成功提交
            transaction.savepoint_commit(sid)
            for cart in cartList:
                theCart = json.loads(cartList[cart].decode())
                if json.loads(cartList[cart].decode())['is_checked'] == '1':
                    print(theCart)
                    conn.hdel('cart' + str(theCart['user_id']), str(theCart['goods_id']))
            ret['code'] = 200
            ret['message'] = '成功'
        except Exception as e:
            print(e, '=======================')
            transaction.savepoint_rollback(sid)
            # 失败回滚
            ret['code'] = 601
            ret['message'] = '失败'
        return Response(ret)


from django.core.paginator import Paginator


class ShowOrderAPIView(APIView):
    def get(self, request):
        ret = {}
        user_id = request.GET.get('user_id')
        try:
            p = request.GET.get('p')
        except:
            p = 1
        totalOrderList = models.Orders.objects.filter(user_id=user_id).all()
        paginator = Paginator(totalOrderList, 4)
        tOrderList = paginator.page(p)
        oList = []
        for o in tOrderList:
            orderList = models.OrderDetails.objects.filter(user_id=user_id, order_sn=o).all()
            detailList = OrderSerializersModel(orderList, many=True)
            oDict = {}
            oDict['date'] = str(o.create_time)
            oDict['num'] = o.order_sn
            oDict['pay_type'] = o.pay_type
            oDict['tPrice'] = o.money
            oDict['status'] = o.status
            oDict['url'] = 'placeHolder'
            oDict['detailList'] = detailList.data
            oList.append(oDict)
        ret['orderList'] = oList
        ret['totalPage'] = paginator.num_pages
        ret['currentPage'] = p
        ret['code'] = 200
        ret['message'] = '成功'
        return Response(ret)


class SetValueSerializersModel(serializers.ModelSerializer):
    score = serializers.IntegerField(default=0)
    commit = serializers.CharField(default='')

    class Meta:
        model = models.OrderDetails
        fields = '__all__'


class SetValue(APIView):
    def get(self, request):
        id = request.GET.get('id')
        try:
            p = request.GET.get('p')
        except:
            p = 1
        detailList = models.OrderDetails.objects.filter(order_sn=id, is_comment=0).all()
        paginator = Paginator(detailList, 1)
        tOrderList = paginator.page(int(p))
        detailList = SetValueSerializersModel(tOrderList, many=True)
        print(id)
        ret = {}
        ret['detailList'] = detailList.data
        ret['totalPage'] = paginator.num_pages
        ret['currentPage'] = p
        ret['code'] = 200
        ret['message'] = '成功'
        return Response(ret)


class CommentSerializers(serializers.Serializer):
    user_id = serializers.IntegerField()
    goods_id = serializers.IntegerField()
    content = serializers.CharField()  # 内容
    score = serializers.IntegerField()  # 评分
    pid = serializers.IntegerField()
    is_anonymity = serializers.IntegerField()  # 是否匿名

    def create(self, data):
        m = Comment.objects.create(**data)
        return m


class SubComment(APIView):
    def post(self, request):
        ret = {}
        data = request.data.copy()
        data['is_anonymity'] = '0' if data['is_anonymity'] == 'false' else '1'

        print(data)
        comment = CommentSerializers(data=data)
        if comment.is_valid():
            comment.save()
            order_id = int(data['order_id'])
            detail = models.OrderDetails.objects.get(id=order_id)
            detail.is_comment = 1
            detail.save()
            #  判断修改订单状态
            detailList = models.OrderDetails.objects.filter(order_sn=detail.order_sn).all()
            status = 0
            for i in detailList:
                status += i.is_comment
            if status == detailList.count():
                order = models.Orders.objects.filter(orderdetails=detail).first()
                # 如果订单下的所有商品都以评论,状态改成已评论
                order.status = 3
                order.save()
            print(detail)
            ret['code'] = 200
            ret['message'] = '成功'
        else:
            print(comment.errors)
            ret['code'] = 601
            ret['message'] = '失败'
        return Response(ret)


# websocket

# 先维护一个链接池

from dwebsocket.decorators import accept_websocket

conn = {}


@accept_websocket
def finish_order(request, name):
    if request.is_websocket:
        conn[name] = request.websocket
        # 检测是否连接
    for message in request.websocket:
        print(message)
        break


# 如果订单支付方式为货到付款,用户下单成功就会发出信息

def sendMessage(request):
    # 用户支付订单,通过商品表找到该商品的添加者的username
    name = 'root'
    mes = json.dumps({'title': '您有新订单待处理'}, ensure_ascii=False)
    conn[name].send(mes)
    return HttpResponse('ok')
