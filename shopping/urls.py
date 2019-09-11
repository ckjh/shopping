"""shopping URL Configuration

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
from django.urls import path

from django.contrib import admin

from django.urls import path, include
from goods import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sadmin/', include('admin01.urls', namespace='sadmin')),
    path('getCateGoods/', views.GetCateGoodsAPIView.as_view()),
    path('getGoodsGoodsByTag/', views.GetGoodsGoodsByTagAPIView.as_view()),
    path('goodsList/', views.GoodsListAPIView.as_view()),
    path('showGoods/', views.ShowGoodsAPIView.as_view()),
    path('detail/', views.DetailAPIView.as_view()),
    path('commentList/', views.CommentList.as_view()),
    path('getImageCode/', views.getCode),
    path('user/', include('user.urls', namespace='user')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('order/', include('order.urls', namespace='order'))
]
