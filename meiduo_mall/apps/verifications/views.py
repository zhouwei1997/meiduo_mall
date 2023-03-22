# Create your views here.
from django import http
from django.views import View
from django_redis import get_redis_connection

from verifications import constants
from verifications.libs.captcha.captcha import captcha


class ImageCodeView(View):
    """图形验证码"""

    def get(self, request, uuid):
        """
        :param request:
        :param uuid: 唯一识别码，用于唯一标识该图形验证码属于那个用户保存的
        :return:
        """
        # 实现主题业务逻辑：生成、保存、响应图形验证码
        # 生成图形验证码
        text, image = captcha.generate_captcha()

        # 保存图形验证码
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s' % uuid, constants.IMAGE_CODE_REDIS_EXPIRES, text)  # 保存图形验证码到redis，设置过期时间为 300s
        # 响应结果
        return http.HttpResponse(image, content_type='image/jpg')
