# Create your views here.
import json
import logging
import re

from django import http
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django_redis import get_redis_connection

from meiduo_mall.utils.response_code import RETCODE
from users.models import User

logger = logging.getLogger('django')


class MobileCountView(View):
    """判断手机号是否重复"""

    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': 'OK',
            'count': count
        })


class UsernameCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        """
        :param username:用户名
        :param request:请求对象
        :return JSON
        """
        # 实现主题业务逻辑 使用username查询对应的记录的条数(filter返回的是满足条件的结果集)
        count = User.objects.filter(username=username).count()
        # 响应结果
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': 'OK',
            'count': count
        })


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
        sms_code_client = request.POST.get('sms_code')  # 短信验证码
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
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号')
        # 判断短信验证码是否合法
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None:
            return render(
                request, 'register.html', {
                    'sms_code_errmsg': '验证码已失效'})
        if sms_code_client != sms_code_server.decode():
            return render(
                request, 'register.html', {
                    'sms_code_errmsg': '短信验证码输入有误'})
        # 判断用户是否勾选了协议
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')
        # 保存注册数据：注册业务核心
        try:
            user = User.objects.create_user(
                username=username, password=password, mobile=mobile)
        except DatabaseError:
            return render(
                request, 'register.html', {
                    'register_errmsg': '注册失败'})
        # 实现会话保持
        login(request, user)
        # 响应结果  重定向到首页
        # return redirect(reverse('contents:index'))
        # 响应结果：重定向到首页
        response = redirect(reverse('contents:index'))
        # 用户名缓存到cookie中
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        # 响应结果：重定向到首页
        return response


class LoginView(View):
    """用户登录"""

    def get(self, request):
        """提供用户登录页面"""
        return render(request, 'login.html')

    def post(self, request):
        """实现用户登录逻辑"""
        # 接受参数
        username = request.POST.get('username')  # 用户名
        password = request.POST.get('password')  # 密码
        remembered = request.POST.get('remembered')  # 记住登录
        # 校验参数
        if not all([username, password]):  # 判断参数是否齐全
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):  # 判断用户名是否是5-20个字符
            return http.HttpResponseForbidden('请输入正确的用户名或手机号')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):  # 判断密码是否是8-20个字符
            return http.HttpResponseForbidden('密码最少为8位，最长为20位')
        # 认证登录用户：使用账号查询用户是否存在，如果用户存在，在校验密码是否正确
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'account_errmsg': '账号或密码错误'})
        # 会话保持：保持登录状态
        login(request, user)
        # 设置状态保持的周期
        if remembered != 'on':
            # 没有记住用户，浏览器会话结束就过期
            request.session.set_expiry(0)  # 单位为秒
        else:
            # 记住用户，设置周期为 14天
            request.session.set_expiry(None)
        # 响应结果：重定向到首页
        next = request.GET.get('next')
        if next:
            # 重定向到next
            response = redirect(next)
        else:
            # 重定向到首页
            response = redirect(reverse('contents:index'))
        # 用户名缓存到cookie中
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        # 响应结果：重定向到首页
        return response


class LogoutView(View):
    """用户退出登录"""

    def get(self, request):
        """实现退出登录逻辑"""
        # 清除状态保持信息
        logout(request)
        # 删除cookie中的用户名
        response = redirect(reverse('contents:index'))
        response.delete_cookie('username')
        # 响应结果：重定向到首页
        return response


class UserInfoView(LoginRequiredMixin, View):
    """用户中心"""

    def get(self, request):
        """提供个人信息页面"""

        #  如果LoginRequiredMixin判断出用户已登录，那么request.user就是用户对象
        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active
        }
        return render(request, 'user_center_info.html', context)


class EmailView(View):
    """添加邮箱"""

    def put(self, request):
        email = json.loads(request.body.decode()).get('email')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('参数email有误')
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({
                'code': RETCODE.DBERR,
                'errmsg': '添加邮箱失败'
            })
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': '添加邮箱成功'
        })
