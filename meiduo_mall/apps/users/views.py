# Create your views here.

import re

from django import http
from django.db import DatabaseError
from django.shortcuts import render
from django.views import View
from users.models import User


class RegisterView(View):
    """用户注册"""

    def get(self, request):
        """提供用户注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        """用户注册业务逻辑"""
        # 接受参数：表单数据
        username = request.POST.get('username')  # 用户名
        password = request.POST.get('password')  # 密码
        password2 = request.POST.get('password2')  # 确认密码
        mobile = request.POST.get('mobile')  # 手机号
        allow = request.POST.get('allow')  # 是否同意用户协议
        """
        校验参数
        前后端校验需要分开
        避免恶意用户越过前端逻辑发起请求，保证后端数据安全
        前后端校验逻辑相同
        """
        # 判断参数是否齐全  all([列表]) 会去校验列表中的元素是否为空，只要有一个为空，返回False
        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个字符
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20个字符的密码')
        # 判断两次输入的密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号是否是11个字符
        if not re.match(r'^1[3-9]\d(9)$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号')
        # 判断用户是否勾选了协议
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')
        # 保存注册数据：注册业务核心
        try:
            User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})
        # 响应结果-- 重定向到首页
        return http.HttpResponse('注册成功，重定向到首页')
