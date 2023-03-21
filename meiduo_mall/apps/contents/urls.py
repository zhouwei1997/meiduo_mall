# -*- coding:utf-8 -*-
"""
# @author ZhouWei
# @date  2023/3/21
# @file  urls.py
# @description
"""
from django.conf.urls import url

from contents.views import IndexView

urlpatterns = [
    url(r'^$', view=IndexView.as_view(), name='index'),  # 首页广告
]
