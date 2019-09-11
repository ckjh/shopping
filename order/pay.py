from django.shortcuts import render, redirect
# 导包
from django.http import HttpResponse, HttpResponseRedirect
# 导入类视图
from django.views import View
import os
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.serializers import serialize
from django.db import connection
import time
import datetime
from .pay1 import AliPay


# 初始化阿里支付对象
def get_ali_object():
    # 沙箱环境地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info
    app_id = "2016101300676523"  # APPID （沙箱应用）

    # 支付完成后，支付偷偷向这里地址发送一个post请求，识别公网IP,如果是 192.168.20.13局域网IP ,支付宝找不到，def page2() 接收不到这个请求
    notify_url = "http://127.0.0.1:8000/md_tast/page1_"
    # notify_url = "http://127.0.0.1:8000/md_tast/page1_"+id

    # 支付完成后，跳转的地址。
    return_url = "http://127.0.0.1:8000/md_tast/page1_"
    app_private_key_path = "./keys/selfkey.txt"  # 应用私钥
    alipay_public_key_path = "./keys/public.txt"  # 支付宝公钥

    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=app_private_key_path,
        alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,  # 默认False,
    )
    return alipay


# def PaGe(request,id):
#     if request.method == "GET":
#         Order.objects.filter(id=id).update(status='已支付')
#         return redirect('http://127.0.0.1:8080/user_center_order.html')


from order.models import Orders



def page1(request):
    if request.method == "GET":
        # 根据当前用户的配置，生成URL，并跳转。
        id = request.GET.get('order_id')
        orders = Orders.objects.filter(order_sn=id).first()
        money = float(orders.money)
        print(money)
        alipay = get_ali_object()

        # 生成支付的url
        query_params = alipay.direct_pay(
            subject="test",  # 商品简单描述
            out_trade_no=orders.order_sn,  # 用户购买的商品订单号（每次不一样） 20180301073422891
            total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
        )

        pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)  # 支付宝网关地址（沙箱应用）
        mes = {}
        mes['code'] = 200
        mes['path'] = pay_url
        return HttpResponse(json.dumps(mes))
