import os
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response

from static.admin.tinymce.response_code import RET, error_map
from rest_framework.views import APIView
from admin01.admin_serializers import *
from django.conf import settings


# Create your views here.

# 注册管理员
def reg(request):
    #  password=make_password(password)
    models.Aadmin.objects.create(username='qaz', pwd=make_password('qaz'))
    return HttpResponse('ok')


def log(request):
    # return render(request,'templates\admin\login.html')
    return render(request, 'admin/login.html')


class LoginView(View):
    def post(self, request):
        ret = {}
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        print(name)
        # 判断参数是否全
        if not all([name, pwd]):
            ret['code'] = RET.DATAERR
            ret['message'] = error_map[RET.DATAERR]
        else:
            admin = models.User.objects.filter(username=name).first()
            # 判断用户名是否存在
            if admin:
                # 判断密码是否正确
                if check_password(pwd, admin.password):
                    request.session['admin_id'] = admin.id
                    ret['code'] = RET.OK
                    ret['message'] = error_map[RET.OK]
                else:
                    ret['code'] = RET.PWDERR
                    ret['message'] = error_map[RET.PWDERR]
            else:
                ret['code'] = RET.USERERR
                ret['message'] = error_map[RET.USERERR]
        return HttpResponse(json.dumps(ret))


def index(request):
    admin_id = request.session.get('admin_id')
    user = models.User.objects.get(id=admin_id)
    role = models.Role.objects.filter(user=user).first()
    resource_list = models.Resource.objects.filter(connect__role_id=role).all()
    return render(request, 'admin/index.html', locals())


def add_cate(request):
    cate_list = models.Cate.objects.all()
    top_cate_list = models.Cate.objects.filter(pid=0)
    return render(request, 'admin/add_cate.html', locals())


def catelist(request):
    return render(request, 'admin/cate_list.html')


class CateList(APIView):
    def get(self, request):
        ret = {}
        cate_list = models.Cate.objects.all()
        ser = CateSerializersModel(cate_list, many=True)

        ret['cate_list'] = ser.data
        ret['code'] = 200
        print(ret)
        return Response(ret)


class DeleteCate(APIView):
    def post(self, request):
        ret = {}
        try:
            id = request.POST.get('id')
            models.Cate.objects.get(id=id).delete()
            print(id)
            ret['code'] = RET.OK
            ret['message'] = error_map[RET.OK]
        except:
            ret['code'] = RET.DBERR
            ret['message'] = error_map[RET.DBERR]
        return Response(ret)


def upload_pic(pic):
    """
    上传图片
    :param pic: 文件
    :return: 路径
    """
    if pic:
        f = open(os.path.join(settings.STATICFILES_DIRS[0], '', pic.name), 'wb')
        for chunk in pic.chunks():
            f.write(chunk)
        f.close()
        return 'http://127.0.0.1:8000/static/' + pic.name


class AddCateView(APIView):

    def post(self, request):
        # 上传图片
        mes = {}
        pic = request.FILES.get('pic')
        try:
            path = upload_pic(pic)
        except Exception as e:
            print(e)
            mes['code'] = RET.PARAMERR
            mes['message'] = error_map[RET.PARAMERR]
            return Response(mes)
        data = request.data
        print('加图前', data)
        data['pic'] = path
        print(data)
        try:
            pid = int(data['pid'])
        except:
            pid = 0
        if pid == 0:
            type = 1
            top_id = 0
        else:
            cate = models.Cate.objects.get(id=pid)
            type = cate.type + 1
            if cate.top_id == 0:
                top_id = cate.id
            else:
                top_id = cate.top_id
        print('加图后', data)
        data['type'] = type
        data['top_id'] = top_id
        c = CateSerializers(data=data)
        if c.is_valid():
            c.save()
            mes['code'] = RET.OK
        else:
            print(c.errors)
            mes['code'] = RET.DATAERR
        return Response(mes)


class EditCateAPIView(APIView):
    def get(self, request):
        ret = {}
        try:
            id = request.GET.get('id')
            print(id)
            cate = models.Cate.objects.get(id=id)
            cate_list = models.Cate.objects.all()
            print(cate, cate_list)
            return render(request, 'admin/edit_cate.html', locals())
        except:
            ret['code'] = RET.DBERR
            ret['message'] = error_map[RET.DBERR]
        return Response(ret)

    def post(self, request):
        # 上传图片
        # 判断是否上传图片,一旦上传图片就使用序列化类
        mes = {}
        try:
            data = request.data
        except Exception as e:
            print(e)
            mes['code'] = RET.PARAMERR
            mes['message'] = error_map[RET.PARAMERR]
            return Response(mes)
        # 通过逻辑判读,得到顶级分类id,和级别
        try:
            pid = int(data['pid'])
        except:
            pid = 0
        if pid == 0:
            type = 1
            top_id = 0
        else:
            cate = models.Cate.objects.get(id=pid)
            type = cate.type + 1
            if cate.top_id == 0:
                top_id = cate.id
            else:
                top_id = cate.top_id

        # print(type(type),type(top_id))
        # 得到顶级分类id, 和级别
        data['type'] = type
        data['top_id'] = top_id
        id, name, is_recommend, pic = data['id'], data['name'], data['is_recommend'], data['pic']
        cate = models.Cate.objects.get(id=id)
        cate.is_recommend = is_recommend
        cate.name = name
        cate.pid = pid
        cate.type = str(type)
        cate.top_id = str(top_id)
        # 接下来存图片
        if pic:
            path = upload_pic(pic)
            data['pic'] = path
            c = CateSerializers(cate, data)
            if c.is_valid():
                c.save()
        else:
            cate.save()
        mes['code'] = RET.DBERR
        mes['message'] = error_map[RET.DBERR]
        return Response(mes)


# 和标签相关
def tag_list(request):
    """展示所有标签"""
    return render(request, 'admin/tags_list.html')


def news_list(request):
    """展示所有标签"""
    return render(request, 'admin/news_list.html')


class TagAPIView(APIView):
    """提供数据"""

    def get(self, request):
        ret = {}
        cate_list = models.Tags.objects.all()
        ser = TagSerializersModel(cate_list, many=True)
        ret['tags_list'] = ser.data
        ret['code'] = 200
        print(ret)
        return Response(ret)


class NewsAPIView(APIView):
    """提供数据"""

    def get(self, request):
        ret = {}
        news_list = models.News.objects.all()
        ser = NewsSerializersModel(news_list, many=True)
        ret['news_list'] = ser.data
        ret['code'] = 200
        print(ret)
        return Response(ret)


def add_tag(request):
    cate_list = models.Cate.objects.filter(pid=0)
    return render(request, 'admin/add_tag.html', locals())


def add_news(request):
    return render(request, 'admin/add_news.html')


class AddTagsAPIView(APIView):
    def post(self, request):
        ret = {}
        data = request.data
        t = TagSerializers(data=data)
        if t.is_valid():
            t.save()
            ret['code'] = RET.OK
        else:
            ret['code'] = RET.DATAERR
        return Response(ret)


class AddNewsAPIView(APIView):
    def post(self, request):
        ret = {}
        data = request.data
        print(data)
        n = NewsSerializers(data=data)
        if n.is_valid():
            n.save()
            ret['code'] = RET.OK
        else:
            print(n.errors)
            ret['code'] = RET.DATAERR
        return Response(ret)


class DeleteTag(APIView):
    def post(self, request):
        ret = {}
        try:
            id = request.POST.get('id')
            models.Tags.objects.get(id=id).delete()
            print(id)
            ret['code'] = RET.OK
            ret['message'] = error_map[RET.OK]
        except:
            ret['code'] = RET.DBERR
            ret['message'] = error_map[RET.DBERR]
        return Response(ret)


class EditTag(APIView):
    def get(self, request):
        ret = {}
        try:
            cate_list = models.Cate.objects.filter(pid=0)
            id = request.GET.get('id')
            tag = models.Tags.objects.get(id=id)
            tag = TagSerializersModel(tag, many=False)
            cate = CateSerializersModel(cate_list, many=True)
            ret['cate_list'] = cate.data
            ret['tag'] = tag.data
            ret['code'] = RET.OK
            ret['message'] = error_map[RET.OK]
        except Exception as e:
            print(e)
            ret['code'] = RET.DBERR
            ret['message'] = error_map[RET.DBERR]
        return Response(ret)

    def post(self, request):
        ret = {}
        try:
            id = request.POST.get('id')
            tag = models.Tags.objects.get(id=id)
            t = TagSerializers(tag, request.data)
            if t.is_valid():
                t.save()
                ret['code'] = RET.OK
                ret['message'] = error_map[RET.OK]
        except Exception as e:
            print(e)
            ret['code'] = RET.DBERR
            ret['message'] = error_map[RET.DBERR]
        return Response(ret)


class DeleteNewsAPIView(APIView):
    def post(self, request):
        ret = {}
        try:
            id = request.POST.get('id')
            models.News.objects.get(id=id).delete()
            print(id)
            ret['code'] = RET.OK
            ret['message'] = error_map[RET.OK]
        except:
            ret['code'] = RET.DBERR
            ret['message'] = error_map[RET.DBERR]
        return Response(ret)


class EditNews(APIView):
    def get(self, request):
        ret = {}
        try:
            id = request.GET.get('id')
            news = models.News.objects.get(id=id)
            news = NewsSerializersModel(news, many=False)
            ret['news'] = news.data
            ret['code'] = RET.OK
            ret['message'] = error_map[RET.OK]
        except Exception as e:
            print(e)
            ret['code'] = RET.DBERR
            ret['message'] = error_map[RET.DBERR]
        return Response(ret)

    def post(self, request):
        ret = {}
        try:
            id = request.POST.get('id')
            tag = models.News.objects.get(id=id)
            n = NewsSerializers(tag, request.data)
            if n.is_valid():
                n.save()
                ret['code'] = RET.OK
                ret['message'] = error_map[RET.OK]
        except Exception as e:
            print(e)
            ret['code'] = RET.DBERR
            ret['message'] = error_map[RET.DBERR]
        return Response(ret)


def showBanner(request):
    return render(request, 'admin/banner_list.html')


class BannerListAPIView(APIView):
    def get(self, request):
        ret = {}
        banner_list = models.Banner.objects.all()
        ser = BannerSerializersModel(banner_list, many=True)
        ret['banner_list'] = ser.data
        ret['code'] = 200
        print(ret)
        return Response(ret)


class AddBannerAPIView(APIView):
    def get(self, request):
        return render(request, 'admin/add_banner.html')

    def post(self, request):
        ret = {}
        try:
            data = request.data
            data['name'] = upload_pic(data['name'])
            print(data)
            d = BannerSerializers(data=data)
            if d.is_valid():
                d.save()
                ret['code'] = RET.OK
            else:
                print(d.errors)
                ret['code'] = RET.DATAERR
        except Exception as e:
            print(e)
            ret['code'] = RET.DBERR
            ret['message'] = error_map[RET.DATAERR]
        return Response(ret)


class DeleteBannerAPIView(APIView):
    def post(self, request):
        ret = {}
        try:
            id = request.POST.get('id')
            models.Banner.objects.get(id=id).delete()
            print(id)
            ret['code'] = RET.OK
            ret['message'] = error_map[RET.OK]
        except:
            ret['code'] = RET.DBERR
            ret['message'] = error_map[RET.DBERR]
        return Response(ret)


class EditBannerAPIView(APIView):
    def get(self, request):
        ret = {}
        try:
            id = request.GET.get('id')
            banner = models.Banner.objects.get(id=id)
            banner = BannerSerializersModel(banner, many=False)
            ret['banner'] = banner.data
            ret['code'] = RET.OK
            ret['message'] = error_map[RET.OK]
            print(ret)
        except Exception as e:
            print(e)
            ret['code'] = RET.DBERR
            ret['message'] = error_map[RET.DBERR]
        return Response(ret)

    def post(self, request):
        ret = {}
        try:
            id = request.POST.get('id')
            tag = models.Banner.objects.get(id=id)
            data = request.data
            data['name'] = upload_pic(data['name'])
            print(data)
            n = BannerSerializers(tag, data)
            if n.is_valid():
                print(id)
                n.save()
                ret['code'] = RET.OK
                ret['message'] = error_map[RET.OK]
                print(ret)
            else:
                print(n.errors)
        except Exception as e:
            print(e)
            ret['code'] = RET.DBERR
            ret['message'] = error_map[RET.DBERR]
        return Response(ret)


def showGoods(request):
    return render(request, 'admin/goods_list.html')


class GoodsListAPIView(APIView):
    def get(self, request):
        ret = {}
        g_list = models.Goods.objects.all()
        ser = GoodsSerializersModel(g_list, many=True)
        ret['goods_list'] = ser.data
        ret['code'] = 200
        print(ret)
        return Response(ret)


def addGoods(request):
    cateList = models.Cate.objects.all()
    tagList = models.Tags.objects.all()
    return render(request, 'admin/add_goods.html', locals())


class AddGoodsAPIView(APIView):
    def get(self, request):
        id = request.GET.get('id')
        goods = models.Goods.objects.get(id=id)
        cateList = models.Cate.objects.all()
        tagList = models.Tags.objects.all()
        return render(request, 'admin/add_goods.html', locals())

    def post(self, request):
        ret = {}
        id = request.POST.get('id')
        # img = request.POST.get('img')
        try:
            data = request.data
            pic = data['pic']
            print(pic.name)

            # 拿到top_id
            try:
                pid = int(data['cid'])
            except:
                pid = 0
            if pid == 0:
                top_id = 0
            else:
                cate = models.Cate.objects.get(id=pid)
                if cate.top_id == 0:
                    top_id = cate.id
                else:
                    top_id = cate.top_id
            if id and not pic:
                the_goods = models.Goods.objects.get(id=id)
                the_goods.top_id = top_id
                the_goods.desc = data['desc']
                the_goods.name = data['name']
                the_goods.price = data['price']
                the_goods.stock = data['stock']
                the_goods.cid = models.Cate.objects.get(id=int(data['cid']))
                the_goods.tid = models.Tags.objects.get(id=int(data['tid']))
                the_goods.is_recommend = data['is_recommend']
                the_goods.lock_stock = data['lock_stock']
                the_goods.save()
                ret['code'] = RET.OK
                ret['message'] = error_map[RET.OK]
                return Response(ret)
            print(top_id)
            data['top_id'] = top_id
            print('===========================', data)
            # cate = models.Cate.objects.get(id=int(data['cid']))
            # tag = models.Tags.objects.get(id=int(data['tid']))
            # print(cate, tag)
            pic = data['pic']
            path = upload_pic(pic)
            data['pic'] = path
            goods_id = request.POST.get('id')
            if goods_id:
                the_goods = models.Goods.objects.get(id=goods_id)
                g = GoodsSerializers(the_goods, data)
                if g.is_valid():
                    print('修改中')
                    g.save()
                    ret['code'] = RET.OK
                    ret['message'] = error_map[RET.OK]
                else:
                    print(g.errors)
            else:
                goods = GoodsSerializers(data=data)
                if goods.is_valid():
                    goods.save()
                    ret['code'] = RET.OK
                    ret['message'] = error_map[RET.OK]
                else:
                    print(goods.errors)

        except Exception as e:
            print(e)
            ret['code'] = RET.DBERR
            ret['message'] = error_map[RET.DBERR]
        return Response(ret)


class DeleteGoodsAPIView(APIView):
    def post(self, request):
        ret = {}
        try:
            id = request.POST.get('id')
            models.Goods.objects.get(id=id).delete()
            print(id)
            ret['code'] = RET.OK
            ret['message'] = error_map[RET.OK]
        except:
            ret['code'] = RET.DBERR
            ret['message'] = error_map[RET.DBERR]
        return Response(ret)


def userList(request):
    return render(request, 'admin/user_list.html')


def roleList(request):
    return render(request, 'admin/role_list.html')


def resourseList(request):
    return render(request, 'admin/resource_list.html')


class GetResourceAPIView(APIView):
    def get(self, request):
        ret = {}
        g_list = models.Resource.objects.all()
        ser = ResourceSerializersModel(g_list, many=True)
        ret['resource_list'] = ser.data
        ret['code'] = 200
        print(ret)
        return Response(ret)


class GetUserAPIView(APIView):
    def get(self, request):
        ret = {}
        g_list = models.User.objects.all()
        ser = UserSerializersModel(g_list, many=True)
        ret['user_list'] = ser.data
        ret['code'] = RET.OK
        print(ret)
        return Response(ret)


class GetRoleAPIView(APIView):
    def get(self, request):
        ret = {}
        c_list = models.Connect.objects.all()
        r_list = models.Role.objects.all()
        c = ConnSerializersModel(c_list, many=True)
        r = RoleSerializersModel(r_list, many=True)
        ret['c_list'] = c.data
        ret['r_list'] = r.data
        ret['code'] = 200
        print(ret)
        return Response(ret)


class DeleteResourceAPIView(APIView):
    def post(self, request):
        ret = {}
        try:
            id = request.POST.get('id')
            models.Resource.objects.get(id=id).delete()
            print(id)
            ret['code'] = RET.OK
            ret['message'] = error_map[RET.OK]
        except:
            ret['code'] = RET.DBERR
            ret['message'] = error_map[RET.DBERR]
        return Response(ret)


class DeleteRoleAPIView(APIView):
    def post(self, request):
        ret = {}
        try:
            id = request.POST.get('id')
            print(id)
            models.Role.objects.get(id=id).delete()
            print(id)
            ret['code'] = RET.OK
            ret['message'] = error_map[RET.OK]
        except Exception as e:
            print(e)
            ret['code'] = RET.DBERR
            ret['message'] = error_map[RET.DBERR]

        return Response(ret)


class DeleteUserAPIView(APIView):
    def post(self, request):
        ret = {}
        try:
            id = request.POST.get('id')
            models.User.objects.get(id=id).delete()
            print(id)
            ret['code'] = RET.OK
            ret['message'] = error_map[RET.OK]
        except:
            ret['code'] = RET.DBERR
            ret['message'] = error_map[RET.DBERR]
        return Response(ret)


class AddResourceAPIView(APIView):
    def get(self, request):
        id = request.GET.get('id')
        if id:
            resource = models.Resource.objects.get(id=id)
        return render(request, 'admin/add_resource.html', locals())

    def post(self, request):
        ret = {}
        data = request.data
        id = request.POST.get('id')
        if not id:
            r = ResourceSerializers(data=data)
            if r.is_valid():
                r.save()
                ret['code'] = RET.OK
            else:
                print(r.errors)
        else:
            resource = models.Resource.objects.get(id=id)
            print(data)
            r = ResourceSerializers(resource, data)
            if r.is_valid():
                r.save()
                ret['code'] = RET.OK
                print('修改成功')
            else:
                print(r.errors)
        return Response(ret)


class AddRoleAPIView(APIView):
    def get(self, request):
        print('===================================')
        id = request.GET.get('id')
        resource_list = models.Resource.objects.all()
        if id:
            role = models.Role.objects.get(id=id)
            resource = models.Resource.objects.filter(connect__role_id=role)
        return render(request, 'admin/add_role.html', locals())

    def post(self, request):
        ret = {}
        data = request.data
        print(data)
        id = request.POST.get('id')
        if not id:
            r = RoleSerializers(data=data)
            if r.is_valid():
                r.save()
                for r_id in request.POST.getlist('resource'):
                    role = models.Role.objects.filter(name=data['name']).first()
                    print(role)
                    models.Connect.objects.create(role_id=role, resource_id_id=r_id)
                ret['code'] = RET.OK
            else:
                print(r.errors)
        else:
            role = models.Role.objects.get(id=id)
            r = RoleSerializers(role, data)
            if r.is_valid():
                models.Connect.objects.filter(role_id=role).delete()
                r.save()
                for r_id in request.POST.getlist('resource'):
                    models.Connect.objects.create(role_id=role, resource_id_id=r_id)
                ret['code'] = RET.OK
            else:
                print(r.errors)

        return Response(ret)


class AddUserAPIView(APIView):
    def get(self, request):
        role_list = models.Role.objects.all()
        id = request.GET.get('id')
        if id:
            user = models.User.objects.get(id=id)
            return render(request, 'admin/add_user.html', locals())
        else:
            return render(request, 'admin/add_user01.html', locals())

    def post(self, request):
        ret = {}
        data = request.data

        print(data)
        id = request.POST.get('id')
        print(id)
        if id == None:
            print('在注册:', data)
            u = UserSerializers(data=data)
            if u.is_valid():
                print('在注册:', data)
                u.save()
                ret['code'] = RET.OK
            else:
                print(u.errors, '=======================')
                ret['code'] = RET.DBERR
        else:
            user = models.User.objects.get(id=id)
            u = UserSerializers(user, data)
            if u.is_valid():
                u.save()
                print('在修改:', data)
                ret['code'] = RET.OK
            else:
                print(u.errors)

        return Response(ret)


# class UserEChart(APIView):
#     def post(self, request):
#         ret = {}
#         ret['code'] = 200
#         ret['message'] = '成功'
#         return Response(ret)

from user.models import Client
from datetime import datetime, timedelta


def userEChart(request):
    # 用户总数
    tCount = Client.objects.count()
    # 用户月活跃数
    startTime = datetime.strftime(datetime.now(), '%Y-%m-01')

    mCount = Client.objects.filter(last_login__gte=startTime, last_login__lt=datetime.now()).count()
    # 用户日活跃数
    dStartTime = datetime.strftime(datetime.now(), '%Y-%m-%d')
    dCount = Client.objects.filter(last_login__gte=dStartTime, last_login__lte=datetime.now()).count()
    # 一个月中每天注册的人
    dateList = []
    countList = []
    for i in range(30, 0, -1):
        print(i)
        sTime = datetime.strptime(startTime, '%Y-%m-%d') - timedelta(i)
        eTime = datetime.strptime(startTime, '%Y-%m-%d') - timedelta(i - 1)
        count = Client.objects.filter(last_login__gte=sTime, last_login__lte=eTime).count()
        countList.append(count)
        dateList.append(datetime.strftime(sTime, '%Y-%m-%d'))
    print(dateList)
    print(countList)
    return render(request, 'admin/user_count.html', locals())

