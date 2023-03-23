# Create your views here.
import json

from django import http
from django.views import View
from django_redis import get_redis_connection
from ronglian_sms_sdk import SmsSDK

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


class CCP(object):
    """发送短信验证码的单例类"""

    def __new__(cls, *args, **kwargs):
        """
        定义单例的初始化方法
        判断单例是否存在，如果存在，初始化。返回单例
        :param args:
        :param kwargs:
        :return 单例
        """
        # _instance 属性中存储的就是单例
        if not hasattr(cls, '_instance'):
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            # 初始化单例
            cls._instance.sdk = SmsSDK(constants.ACCOUNT_SID, constants.AUTH_TOKEN, constants.APP_ID)
        return cls._instance

    def send_template(self, tid, mobile, datas):
        """
        发送短信验证码单例方法
        :param datas: 内容数据
        :param tid: 模板ID
        :param mobile: 手机号
        :return: 成功 0  失败 -1
        """
        response = json.loads(self.sdk.sendMessage(tid, mobile, datas))
        if response.get('statusCode') == '000000':
            return 0
        else:
            return -1


class SmsCodeView(View):
    """短信验证码"""
    pass

# if __name__ == '__main__':
#     ccp = CCP()
#     ccp.send_template('1', '15027130472', ['123456', '5分钟'])
