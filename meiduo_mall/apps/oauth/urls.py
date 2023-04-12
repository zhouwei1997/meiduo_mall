# -*- coding:utf-8 -*-
"""
# @author ZhouWei
# @date  2023/4/12
# @file  urls.py
# @description
"""
from django.conf.urls import url

from oauth import views

urlpatterns = [
    # 提供QQ登录扫码页面
    url(r'^qq/login/$', views.QQAuthURLView.as_view()),
    # 提供QQ登录扫码页面
    url(r'^oauth_callback/$', views.QQAuthUserView.as_view()),
]
