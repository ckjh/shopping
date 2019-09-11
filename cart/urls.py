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

from django.urls import path, include
from cart import views

app_name = 'cart'
urlpatterns = [
    path('', views.CartListAPIView.as_view()),
    path('addCart/', views.AddCartAPIView.as_view()),
    path('deleteCart/', views.DeleteCartAPIVIew.as_view()),
    path('addReduce/', views.AddReduceCountAPIView.as_view()),
    path('submitCart/', views.SubmitCartAPIView.as_view())
]
