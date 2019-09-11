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
from order import views
from order import pay

app_name = 'order'
urlpatterns = [
    path('createOrder/', views.CreateOrderAPIView.as_view()),
    path('showOrder/', views.ShowOrderAPIView.as_view()),
    path('showOrderDetail/', views.SetValue.as_view()),
    path('pay/', pay.page1),
    path('subComment/', views.SubComment.as_view()),
    path('finish_order/<str:name>', views.finish_order),
    path('sendMessage/', views.sendMessage),
]
