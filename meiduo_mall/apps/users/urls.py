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
    # 判断用户名是否重复
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view()),
    # 判断手机号是否重复
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    # 用户登录
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    # 用户退出登录
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    # 用户中心
    url(r'^info/$', views.UserInfoView.as_view(), name='info'),
    # 添加邮箱
    url(r'^emails/$', views.EmailView.as_view()),
    # 验证邮箱
    url(r'^emails/verification/$', views.VerifyEmailView.as_view()),
    # 展示收货地址
    url(r'^addresses/$', views.AddressView.as_view(), name='address'),
    # 新增用户地址
    url(r'^addresses/create/$', views.AddressCreateView.as_view()),
    # 修改和删除收货地址
    url(r'^addresses/(?P<address_id>\d+)/$', views.UpdateDestroyAddressView.as_view()),
    # 设置默认地址
    url(r'^addresses/(?P<address_id>\d+)/default/$', views.DefaultAddressView.as_view()),
    # 修改地址标题
    url(r'^addresses/(?P<address_id>\d+)/title/$', views.UpdateTitleAddressView.as_view()),
]
