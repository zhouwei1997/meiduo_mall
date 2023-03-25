# -*- coding:utf-8 -*-
"""
# @author ZhouWei
# @date  2023/3/22
# @file  urls.py
# @description 验证码路由
"""
from django.conf.urls import url

from verifications import views

urlpatterns = [
    # 图形验证码
    url(r'^image_codes/(?P<uuid>[\w-]+)/$', views.ImageCodeView.as_view()),
    # 短信验证码
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
]
