from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from user.models import Client, City, Address
from rest_framework.response import Response
from admin01.admin_serializers import *
from django.http import HttpResponse
from static.admin.tinymce.response_code import RET, error_map
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.core.mail import send_mail
from user.task import sendEmail
import json
import uuid
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_name.settings")
django.setup()


class UserAddressSerializersModel(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class UserSerializersModel(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class UserSerializers(serializers.Serializer):
    username = serializers.CharField(allow_null=False)
    password = serializers.CharField(allow_null=False)
    email = serializers.CharField(allow_null=False)
    token = serializers.CharField(allow_null=False)

    def create(self, data):
        user = Client.objects.create(username=data['username'],
                                     password=make_password(data['password']),
                                     email=data['email'],
                                     token=data['token'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        修改地址
        :param instance:
        :param validated_data:
        :return:
        """
        instance.username = validated_data['username']
        instance.password = validated_data['password']
        instance.email = validated_data['email']
        instance.pic = validated_data['pic']
        instance.is_valid = validated_data['is_valid']
        instance.signature = validated_data['signature']
        instance.token = validated_data['token']
        return instance


class RegAPIView(APIView):
    def post(self, request):
        ret = {}
        code = request.session.get('imageCode')
        print(code)
        data = request.data
        if code != str(data['imagecode']).upper():
            ret['code'] = 607
            ret['message'] = '验证码错误'
        else:
            user = data['username']
            pwd = data['password']
            if not (5 < len(user) < 20 or 8 < len(pwd) < 20):
                ret['code'] = 608
                ret['message'] = '密码或账号长度错误'
            else:
                try:
                    # 生成token,
                    token = makeTokenByuuid(data)
                    # 发送激活连接
                    send(token, data['email'])
                    ret['code'] = 200
                    ret['message'] = '注册成功'
                except Exception as ex:
                    print(ex, '===================================')
                    ret['code'] = 700
                    ret['message'] = 'token过期,或用户名已存在'
        return Response(ret)


def send(token, email):
    """同步"""
    if token == str(token):
        pass
    else:
        token = token.decode()
    title = '欢迎注册美多商城'
    content = '<a href="http://127.0.0.1:8000/user/active/?token=' + token + '">点击激活账号</a>'
    send_mail(title, content, settings.EMAIL_FORM, [email], html_message=content)


def makeTokenByitsdangerous(data):
    """使用itsdangerous生成token"""
    from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
    one_user = Client.objects.create(username=data['username'],
                                     password=make_password(data['password']),
                                     email=data['email'])
    serializer = Serializer(settings.SECRET_KEY, 3600)
    user_info = {'user_id': one_user.id}
    token = serializer.dumps(user_info)
    return token


def useTokenmadeByitsdangerous(token):
    from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
    serializer = Serializer(settings.SECRET_KEY, 3600)
    user_info = serializer.loads(token)
    user_id = user_info['user_id']
    user = Client.objects.filter(id=user_id).first()
    return user


def makeTokenByuuid(data):
    """使用uuid生成Token"""
    import uuid
    token = str(uuid.uuid1())
    print(data)
    u = UserSerializers(
        data={'username': data['username'], 'password': data['password'], 'email': data['email'], 'token': token})
    if u.is_valid():
        u.save()
    else:
        print(u.errors)
    return token


def useTokenmadeByuuid(token):
    if str(token) == token:
        pass
    else:
        token = token.encode()
    user = Client.objects.filter(token=token).first()
    return user


class ActiveView(APIView):
    def get(self, request):
        from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
        ret = {'code': 600, 'message': None}
        token = request.GET.get('token')
        print(token)
        # 使用itsdangerous生成的token
        user = useTokenmadeByuuid(token)
        if not user:
            ret['code'] = 601
            ret['message'] = '用户不存在'
            return Response(ret)
        user.is_valid = 1
        user.save()
        ret['code'] = 200
        ret['message'] = '激活成功'
        return Response(ret)


from datetime import datetime


class LoginAPIView(ActiveView):
    def post(self, request):
        ret = {}
        data = request.data
        username = data['username']
        password = data['password']
        user = Client.objects.filter(username=username).first()

        if not user:
            ret['code'] = 612
            ret['message'] = '用户不存在'
        else:
            if user.is_valid == 0:
                ret['code'] = 613
                ret['message'] = '用户名未激活'
            else:
                if not check_password(password, user.password):
                    ret['code'] = 613
                    ret['message'] = '密码错误'

                else:
                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    user.last_login = datetime.now()
                    user.save()
                    ret['token'] = token  # 上面的代码是自定义登录生成token
                    ret['username'] = user.username
                    ret['user_id'] = user.id
                    ret['code'] = 200
                    ret['message'] = '登录成功'
        print(ret, '======================')
        return Response(ret)


class CitySerializersModel(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class AddressSerializersModel(serializers.ModelSerializer):
    """
    省市县三级联动
    """

    class Meta:
        model = City
        fields = '__all__'


class AddressSerializers(serializers.Serializer):
    name = serializers.CharField()
    receiver = serializers.CharField()
    province_id = serializers.IntegerField()
    city_id = serializers.IntegerField()
    district_id = serializers.IntegerField()
    place = serializers.CharField()
    mobile = serializers.CharField()
    tel = serializers.CharField(allow_null=True)
    email = serializers.CharField(allow_null=True)
    user_id = serializers.IntegerField()
    district = serializers.CharField(max_length=50, default='')
    city = serializers.CharField(max_length=50, default='')
    province = serializers.CharField(max_length=50, default='')
    is_default = serializers.IntegerField(default=0)

    def create(self, data):
        """
        新建地址
        :param data:
        :return:
        """
        m = Address.objects.create(**data)

        return m

    def update(self, instance, validated_data):
        """
        修改地址
        :param instance:
        :param validated_data:
        :return:
        """
        instance.name = validated_data['name']
        instance.receiver = validated_data['receiver']
        instance.province_id = validated_data['province_id']
        instance.city_id = validated_data['city_id']
        instance.district_id = validated_data['district_id']
        instance.tel = validated_data['tel']
        instance.email = validated_data['email']
        instance.user_id = validated_data['user_id']
        instance.district = validated_data['district']
        instance.city = validated_data['city']
        instance.province = validated_data['province']
        instance.is_default = validated_data['is_default']
        instance.save()
        return instance


class AddAddress(APIView):
    def post(self, request):
        ret = {}
        data = request.data.copy()
        province = City.objects.get(id=int(data['province_id']))
        city = City.objects.get(id=int(data['city_id']))
        district = City.objects.get(id=int(data['district_id']))
        data['province'] = province.name
        data['city'] = city.name
        data['district'] = district.name
        if province and city and district:
            name = str(province.name) + str(city.name) + str(district.name) + str(data['place']) + "(" + str(
                data['receiver']) + " 收)" + str(data['mobile'])
            data['name'] = name
            # 写反系列化类
            if int(data['edit_id']) == 0:
                address = AddressSerializers(data=data)
            else:
                editAddress = Address.objects.get(id=int(data['edit_id']))
                address = AddressSerializers(editAddress, data)
            if address.is_valid():
                address.save()
                ret['code'] = 200
                ret['message'] = '成功'
            else:
                print(address.errors)
                ret['code'] = 601
                ret['message'] = '添加失败'
        else:
            ret['code'] = 601
            ret['message'] = '失败'
        return Response(ret)


class UserAddress(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        addressList = Address.objects.filter(user_id=user_id).all()
        addressList = UserAddressSerializersModel(addressList, many=True)
        ret = {}
        ret['addressList'] = addressList.data
        ret['code'] = 200
        ret['message'] = '成功'
        return Response(ret)


class DeleteAddress(APIView):
    def post(self, request):
        ret = {}
        try:
            data = request.data
            Address.objects.get(id=int(data['aid'])).delete()
            ret['code'] = 200
            ret['message'] = '成功'
        except:
            ret['code'] = 601
            ret['message'] = '失败'
        return Response(ret)


class SetDefaultAddress(APIView):
    def post(self, request):
        ret = {}
        try:
            data = request.data
            address = Address.objects.get(id=int(data['aid']))
            Address.objects.filter(user_id=address.user_id).all().update(is_default=0)
            address.is_default = 1
            address.save()
            ret['code'] = 200
            ret['message'] = '成功'
        except:
            ret['code'] = 601
            ret['message'] = '失败'
        return Response(ret)


class ShowAddress(APIView):
    def get(self, request):
        cityList = City.objects.all()
        fList = City.objects.filter(level=0).all()
        cityList = AddressSerializersModel(cityList, many=True)
        fList = AddressSerializersModel(fList, many=True)
        ret = {}
        ret['fList'] = fList.data
        # ret['cityList'] = cityList.data
        ret['code'] = 200
        ret['message'] = '成功'
        return Response(ret)


class GetCity(APIView):
    def post(self, request):
        data = request.data
        cList = City.objects.filter(parent_id=int(data['pid']))
        cList = AddressSerializersModel(cList, many=True)
        ret = {}
        ret['cList'] = cList.data
        ret['code'] = 200
        ret['message'] = '成功'
        return Response(ret)


class UserDetail(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        user = Client.objects.get(id=user_id)
        user = UserSerializersModel(user, many=False)
        ret = {}
        ret['user'] = user.data
        ret['code'] = 200
        ret['message'] = '成功'
        return Response(ret)

    def post(self, request):
        ret = {}
        data = request.data
        email = data['email']
        if email:
            user = Client.objects.get(id=int(data['user_id']))
            user.email = email
            user.save()
        ret['code'] = 200
        ret['message'] = '成功'
        return Response(ret)


class ChangePassword(APIView):
    def post(self, request):
        ret = {}
        try:
            data = request.data
            password = data['password']
            newPassword = data['newPassword']
            user_id = data['user_id']
            user = Client.objects.get(id=user_id)
            if 8 < len(newPassword) < 20:
                if check_password(password, user.password):
                    user.password = make_password(newPassword)
                    user.save()
                    ret['code'] = 200
                    ret['message'] = '成功'
                else:
                    ret['code'] = 607
                    ret['message'] = '原密码有误'
            else:
                ret['code'] = 608
                ret['message'] = '新密码长度有误'
        except:
            ret['code'] = 609
            ret['message'] = '修改失败'
        return Response(ret)


class SetPic(APIView):
    def post(self, request):
        ret = {}
        pic = request.FILES.get("pic")
        print("FIFLE", request.FILES)
        print(type(pic))
        ret['code'] = 200
        ret['message'] = '成功'
        return Response(ret)
