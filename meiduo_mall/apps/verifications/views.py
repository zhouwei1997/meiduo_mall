# Create your views here.
import logging
import random

from django import http
from django.views import View
from django_redis import get_redis_connection

from celery_tasks.sms import constants
from meiduo_mall.utils.response_code import RETCODE
from verifications.libs.captcha.captcha import captcha

# 创建日志输出器
logger = logging.getLogger('django')


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


# class CCP(object):
#     """发送短信验证码的单例类"""
#
#     def __new__(cls, *args, **kwargs):
#         """
#         定义单例的初始化方法
#         判断单例是否存在，如果存在，初始化。返回单例
#         :param args:
#         :param kwargs:
#         :return 单例
#         """
#         # _instance 属性中存储的就是单例
#         if not hasattr(cls, '_instance'):
#             cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
#             # 初始化单例
#             cls._instance.sdk = SmsSDK(constants.ACCOUNT_SID, constants.AUTH_TOKEN, constants.APP_ID)
#         return cls._instance
#
#     def send_template(self, tid, mobile, datas):
#         """
#         发送短信验证码单例方法
#         :param datas: 内容数据
#         :param tid: 模板ID
#         :param mobile: 手机号
#         :return: 成功 0  失败 -1
#         """
#         response = json.loads(self.sdk.sendMessage(tid, mobile, datas))
#         if response.get('statusCode') == '000000':
#             return 0
#         else:
#             return -1


class SMSCodeView(View):
    """短信验证码"""

    def get(self, request, mobile):
        """
        :param request: 请求参数
        :param mobile: 手机号
        :return: JSON
        """
        # 接收参数
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        # 校验参数
        if not all([image_code_client, uuid]):
            return http.HttpResponseForbidden('缺少必要参数')
        redis_conn = get_redis_connection('verify_code')
        # 判断用户是否频繁发送短信验证码-提取短信验证码的标记
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return http.JsonResponse({
                'code': RETCODE.THROTTLINGERR,
                'errmsg': '发送短信访问过于频繁'
            })
        # 提取图形验证码
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            return http.JsonResponse({
                'code': RETCODE.IMAGECODEERR,
                'errmsg': '图形验证码已失效'
            })
        # 删除图形验证码
        redis_conn.delete('img_%s' % uuid)
        # 对比图形验证码
        image_code_server = image_code_server.decode()  # 将bytes转字符串在比较
        if image_code_client.lower() != image_code_server.lower():  # 全部转换为小写，然后再比较
            return http.JsonResponse({
                'code': RETCODE.IMAGECODEERR,
                'errmsg': '验证码输入有误'
            })
        # 生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info(sms_code)
        # 创建redis的管道
        pl = redis_conn.pipline()
        # 将命令添加到管道中
        # 保存短信验证码
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        # 执行
        pl.execute()
        # 发送短信验证码
        # CCP().send_template(constants.SEND_SMS_TEMPLATE_ID, mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60])
        # 响应结果
        return http.JsonResponse({
            'code': RETCODE.IMAGECODEERR,
            'errmsg': '短信发送成功'
        })
