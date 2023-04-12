# Create your views here.
import logging

from QQLoginTool.QQtool import OAuthQQ
from django import http
from django.conf import settings
from django.views import View

from meiduo_mall.utils.response_code import RETCODE

# 创建日志输出器
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


class QQAuthURLView(View):
    """提供QQ登录扫码页面"""

    def get(self, request):
        # 接受next
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
