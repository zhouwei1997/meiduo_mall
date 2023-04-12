# Create your views here.
import logging

from QQLoginTool.QQtool import OAuthQQ
from django import http
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from meiduo_mall.utils.response_code import RETCODE
from oauth.models import OAuthQQUser
# 创建日志输出器
from oauth.utils import generate_access_token

logger = logging.getLogger('django')


class QQAuthUserView(View):
    """处理QQ登录回调"""

    def get(self, request):
        """处理QQ回调的逻辑"""
        code = request.GET.get('code')
        if not code:
            return http.HttpResponseForbidden('获取code失败')
        oauth = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            # 使用code获取access_token
            access_token = oauth.get_access_token(code)
            # 获取openid
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            logging.error(e)
            return http.HttpResponseServerError('OAuth2.0认证失败')

        # 使用openid判断该QQ用户是否绑定过
        try:
            oauth_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # openid未绑定用户
            access_token_openid = generate_access_token(openid)
            context = {'access_token_openid': access_token_openid}
            return render(request, 'oauth_callback.html', context)
        else:
            # openid已绑定用户,oauth_user.user表示从QQ登录模型类对象中找到对应的用户模型类对象
            login(request, oauth_user.user)
            # 重定向到首页
            response = redirect(reverse('contents:index'))
            response.set_cookie('username', oauth_user.user.username, max_age=3600 * 24 * 15)
            # 响应结果
            return response

    def post(self, request):
        pass


class QQAuthURLView(View):
    """提供QQ登录扫码页面"""

    def get(self, request):
        # 接受next
        next = request.GET.get('next')
        # 创建工具对象
        oauth = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI, state=next)

        # 生成扫码链接地址
        login_url = oauth.get_qq_url()
        # 响应
        from django import http
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': 'OK',
            'login_url': login_url
        })
