# -*- coding:utf-8 -*-
"""
# @author ZhouWei
# @date  2023/3/20
# @file  urls.py
# @description users的路由信息
"""
from django.conf.urls import url

from users import views

urlpatterns = [
    # 用户注册   reverse(user:register) == '/register/'
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
]
