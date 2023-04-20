# -*- coding:utf-8 -*-
"""
# @author ZhouWei
# @date  2023/4/20
# @file  urls.py
# @description
"""
from django.conf.urls import url

from areas import views

urlpatterns = [
    # 省市区三级联动
    url(r'^areas/$', views.AreaView.as_view())
]
