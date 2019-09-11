"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include
from admin01 import views

urlpatterns = [
    path('login/', views.log),  # 登录页面函数
    path('log', views.LoginView.as_view()),  # 登录验证
    path('', views.index),  # 首页函数
    path('addCate/', views.add_cate),  # 添加分类的页面
    path('cate', views.AddCateView.as_view()),  # 添加分类
    path('cateList/', views.CateList.as_view()),  # 展示分类Ajax
    path('catelist/', views.catelist),  # 展示分类HTML
    path('deleteCate', views.DeleteCate.as_view()),  # 删除分类
    path('editCate', views.EditCateAPIView.as_view()),
    path('showTag/', views.tag_list),  # 展示标签 HTML
    path('tagList/', views.TagAPIView.as_view()),  # 提供标签数据
    path('addTag/', views.AddTagsAPIView.as_view()),  # 接收添加标签的Ajax POST请求
    path('getAddtag/', views.add_tag),  # 渲染HTML页面
    path('deleteTag', views.DeleteTag.as_view()),  # 删除标签
    path('editTag/', views.EditTag.as_view()),
    path('news_list/', views.news_list),
    path('newsList/', views.NewsAPIView.as_view()),
    path('addNews/', views.add_news),
    path('getAddNews/', views.AddNewsAPIView.as_view()),
    path('deleteNews/', views.DeleteNewsAPIView.as_view()),
    path('editNews/', views.EditNews.as_view()),
    path('showBanner/', views.showBanner),
    path('bannerList/', views.BannerListAPIView.as_view()),
    path('addBanner/', views.AddBannerAPIView.as_view()),
    path('deleteBanner/', views.DeleteBannerAPIView.as_view()),
    path('editBanner/', views.EditBannerAPIView.as_view()),
    path('showGoods/', views.showGoods),
    path('goodsList/', views.GoodsListAPIView.as_view()),
    path('addGoods/', views.addGoods),
    path('AddGoods/', views.AddGoodsAPIView.as_view()),
    path('deleteGoods/', views.DeleteGoodsAPIView.as_view()),
    path('userList/', views.userList),
    path('roleList/', views.roleList),
    path('resourseList/', views.resourseList),
    path('getuserList/', views.GetUserAPIView.as_view()),
    path('getroleList/', views.GetRoleAPIView.as_view()),
    path('getresourseList/', views.GetResourceAPIView.as_view()),
    path('deleteResource/', views.DeleteResourceAPIView.as_view()),
    path('deleteRole/', views.DeleteRoleAPIView.as_view()),
    path('deleteUser/', views.DeleteUserAPIView.as_view()),
    path('addUser/', views.AddUserAPIView.as_view()),
    path('addResource/', views.AddResourceAPIView.as_view()),
    path('addRole/', views.AddRoleAPIView.as_view()),
    path('user_count/',views.userEChart)

]
app_name = 'admin01'
