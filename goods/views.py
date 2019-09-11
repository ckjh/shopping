from rest_framework.views import APIView
from admin01 import models
from rest_framework.response import Response
from admin01.admin_serializers import *
from goods.models import Comment
from user.models import Client


# Create your views here.

class GetCateGoodsAPIView(APIView):
    def get(self, request):
        ret = {}
        cate_list = models.Cate.objects.filter(pid=0).all()
        cList = []
        newList = models.News.objects.all()
        newList = NewsSerializersModel(newList, many=True)
        for cate in cate_list:
            cDict = {}  # 一级分类
            cDict['id'] = cate.id
            cDict['name'] = cate.name
            cDict['image'] = cate.pic
            secondCate = models.Cate.objects.filter(pid=cate.id).all()
            sc = CateSerializersModel01(secondCate, many=True)
            cDict['subList'] = sc.data
            tags = models.Tags.objects.filter(cid=cate.id).all()
            t = TagSerializersModel(tags, many=True)
            cDict['tags'] = t.data
            goods = models.Goods.objects.filter(top_id=cate.id).all()
            g = GoodsSerializersModel(goods, many=True)
            cDict['goods'] = g.data
            cList.append(cDict)
        bannerList = models.Banner.objects.filter(is_show=1).all()
        bannerList = BannerSerializersModel(bannerList, many=True)
        ret['newsList'] = newList.data
        ret['bannerList'] = bannerList.data
        ret['code'] = 200
        ret['cateList'] = cList
        return Response(ret)

        # 序列化二级分类

        # return Response(ret)


class GetGoodsGoodsByTagAPIView(APIView):
    def get(self, request):
        cid = request.GET.get('cid')
        tid = request.GET.get('tid')
        print('cid /tid', cid, tid)
        goods = models.Goods.objects.filter(top_id=cid, tid=tid).all()
        goods = GoodsSerializersModel(goods, many=True)
        print(goods.data)
        ret = {}
        ret['code'] = 200
        ret['goods'] = goods.data
        return Response(ret)


class GoodsListAPIView(APIView):
    def get(self, request):
        ret = {}
        goodsList = models.Goods.objects.all().order_by('-sales')
        goodsList = GoodsSerializersModel(goodsList[:2:], many=True)
        ret['goodsList_by_sales'] = goodsList.data
        ret['code'] = 200
        print(ret)
        return Response(ret)


class DetailAPIView(APIView):
    def get(self, request):
        id = request.GET.get('id')
        goods = models.Goods.objects.get(id=id)
        goods = GoodsSerializersModel(goods, many=False)
        ret = {}
        ret['code'] = 200
        ret['goods'] = goods.data
        return Response(ret)


from django.http import HttpResponse
from utils.captcha.captcha import captcha


def getCode(request):
    name, text, image = captcha.generate_captcha()
    request.session['imageCode'] = text
    return HttpResponse(image, 'image/jpg')


from django.core.paginator import Paginator


class ShowGoodsAPIView(APIView):
    def get(self, request):
        ret = {}
        sort = request.GET.get('sort')
        top_id = request.GET.get('top_id')
        cid = request.GET.get('cid')
        try:
            p = request.GET.get('p')
        except:
            p = 1
        print('===============排序', cid)
        if cid == 'undefined':
            GoodsList = models.Goods.objects.filter(top_id=top_id).all().order_by(sort)
        else:
            GoodsList = models.Goods.objects.filter(cid=cid).all().order_by(sort)
        paginator = Paginator(GoodsList, 5)
        GoodsList = paginator.page(int(p))
        GoodsList = GoodsSerializersModel(GoodsList, many=True)
        ret['code'] = 200
        ret['totalPage'] = paginator.num_pages
        ret['currentPage'] = p
        ret['GoodsList'] = GoodsList.data
        ret['message'] = '成功'
        return Response(ret)


class CommentSerializersModel(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, row):
        if row.is_anonymity ==0:
            c = Client.objects.get(id=row.user_id)
            name = c.username
        else:
            name = '匿名'
        return name

    class Meta:
        model = Comment
        fields = '__all__'


class CommentList(APIView):
    def get(self, request):
        ret = {}
        goods_id = request.GET.get('goods_id')
        print(goods_id)
        # 加是否审核
        commentList = Comment.objects.filter(goods_id=int(goods_id)).all()
        commentList = CommentSerializersModel(commentList, many=True)
        ret['commentList'] = commentList.data
        ret['code'] = 200
        ret['message'] = '成功'
        return Response(ret)
