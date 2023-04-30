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
from requests import get

from celery_tasks.email.tasks import send_verify_email
from meiduo_mall.utils.response_code import RETCODE
from meiduo_mall.utils.views import LoginRequiredJSONMinxin
from users import constants
from users.models import User, Address
from users.utils import generate_verify_email_url, check_verify_email_token

logger = logging.getLogger('django')


class UpdateDestroyAddressView(LoginRequiredJSONMinxin, View):
    """修改和删除地址"""

    def put(self, request, address_id):
        """
        修改地址
        :param request:
        :param address_id: 需要更新的地址id
        :return:
        """
        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')
        if not all([receiver, province_id, city_id,
                    district_id, place, mobile]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('参数mobile有误')
        if tel:
            if not re.match(
                    r'^(0(0-9){2,3}-)?([2-9]{6,7})+(-[0-9]{1,4})?$',
                    tel):
                return http.HttpResponseForbidden('参数tel有误')
        if email:
            if not re.match(
                    r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',
                    email):
                return http.HttpResponseForbidden('参数email有误')

        # 判断地址是否存在，并更新地址信息
        try:
            Address.objects.filter(
                id=address_id).update(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({
                'code': RETCODE.DBERR,
                'errmsg': '更新地址失败'
            })
        # 构造响应数据
        address = Address.objects.get(id=address_id)
        address_dict = {
            'id': address.id,
            'title': address.title,
            'receiver': address.receiver,
            'province': address.province.name,
            'city': address.city.name,
            'district': address.district.name,
            'place': address.place,
            'mobile': address.mobile,
            'tel': address.tel,
            'email': address.email
        }
        # 响应更新地址结果
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': '更新地址成功',
            'address': address_dict
        })

    def delete(self, request, address_id):
        """
        删除地址
        :param request:
        :param address_id:需要删除的地址id
        :return: 指定地址的逻辑删除 is_delete = True
        """
        try:
            address = Address.objects.get(id=address_id)
            address.is_delete = True
            address.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({
                'code': RETCODE.DBERR,
                'errmsg': '删除地址失败'
            })
        # 响应更新地址结果
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': '删除地址成功'
        })


class AddressCreateView(LoginRequiredJSONMinxin, View):
    """新增地址"""

    def post(self, reqeust):
        """新增地址"""
        # 判断用户地址数量是否超过上限
        count = reqeust.user.addresses.count()
        if count > constants.USER_ADDRESS_COUNTS_LIMIT:
            return http.JsonResponse({
                'code': RETCODE.THROTTLINGERR,
                'errmsg': '超出用户地址上限'
            })
        # 接受参数
        json_str = reqeust.body.decode()
        json_dict = json.loads(json_str)
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')
        # 校验参数
        if not all([receiver, province_id, city_id,
                    district_id, place, mobile]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^1[3-9]\d(9)$', mobile):
            return http.HttpResponseForbidden('参数mobile有误')
        if tel:
            if not re.match(
                    r'^(0(0-9){2,3}-)?([2-9]{6,7})+(-[0-9]{1,4})?$',
                    tel):
                return http.HttpResponseForbidden('参数tel有误')
        if email:
            if not re.match(
                    r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',
                    email):
                return http.HttpResponseForbidden('参数email有误')
        # 保存用户传入的地址信息
        try:
            address = Address.objects.create(
                user=reqeust.user,
                title=receiver,  # 标题默认就是收货人
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email, )
            # 如果没有默认地址，则新增地址为默认地址
            if not reqeust.user.default_address:
                reqeust.user.default_address = address
                reqeust.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({
                'code': RETCODE.DBERR,
                'errmsg': '新增地址失败'
            })
        # 响应新增地址结果：需要将新增地址渲染到前端
        address_dict = {
            'id': address.id,
            'title': address.title,
            'receiver': address.receiver,
            'province': address.province.name,
            'city': address.city.name,
            'district': address.district.name,
            'place': address.place,
            'mobile': address.mobile,
            'tel': address.tel,
            'email': address.email
        }
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': '新增地址成功',
            'address': address_dict
        })


class AddressView(LoginRequiredMixin, View):
    """用户收货地址"""

    def get(self, request):
        """提供收货地址页面"""
        login_user = request.user
        addresses = Address.objects.filter(user=login_user, is_deleted=False)
        address_list = []
        for address in addresses:
            address_dict = {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email}
            address_list.append(address_dict)
        context = {
            'default_address_id': login_user.default_address_id,
            'addresses': address_list,
        }
        return render(request, 'user_center_site.html', context)


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
        sms_code_server = get('sms_%s' % mobile)
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


class EmailView(LoginRequiredJSONMinxin, View):
    """添加邮箱"""

    def put(self, request):
        email = json.get('email')
        if not re.match(
                r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',
                email):
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
        # 发送邮箱验证
        verify_url = generate_verify_email_url(request.user)
        send_verify_email.delay(email, verify_url)
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': '添加邮箱成功'
        })


class VerifyEmailView(View):
    """验证邮箱"""

    def get(self, request):
        # 接收参数
        token = request.GET.get('token')
        # 校验参数
        if not token:
            return http.HttpResponseForbidden('缺少token')
        # 从token中提取用户的信息 user_id ==> user
        user = check_verify_email_token(token)
        if not user:
            return http.HttpResponseForbidden('无效的token')
        # 将用户的email_active字段设置为True
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('激活邮箱失败')
        # 响应结果：重定向到用户中心
        return redirect(reverse('users:info'))
