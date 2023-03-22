# -*- coding:utf-8 -*-
"""
# @author ZhouWei
# @date  2023/3/22
# @file  urls.py
# @description
"""
from django.conf.urls import url

from verifications import views

urlpatterns = [
    url(r'^image_codes/(?P<uuid>[\w-]+)/$', views.ImageCodeView.as_view())
]
