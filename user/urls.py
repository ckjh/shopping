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
from django.urls import path, re_path

from django.contrib import admin
from user import views

from django.urls import path, include
from user import views
from rest_framework_jwt.views import obtain_jwt_token

app_name = 'user'
urlpatterns = [
    path('reg/', views.RegAPIView.as_view()),
    path('active/', views.ActiveView.as_view()),
    re_path(r'login/', obtain_jwt_token, 'auths'),
    path('log/', views.LoginAPIView.as_view()),
    path('showAddress/', views.ShowAddress.as_view()),
    path('getCity/', views.GetCity.as_view()),
    path('addAddress/', views.AddAddress.as_view()),
    path('addressList/', views.UserAddress.as_view()),
    path('deleteAddress/', views.DeleteAddress.as_view()),
    path('setDefault/', views.SetDefaultAddress.as_view()),
    path('userDetail/', views.UserDetail.as_view()),
    path('changePassword/', views.ChangePassword.as_view()),
    path('setPic/', views.SetPic.as_view())

]
