# -*- coding:utf-8 -*-
"""
# @author ZhouWei
# @date  2023/4/5
# @file  tasks.py
# @description 定义发送短信任务
"""
import json

from ronglian_sms_sdk import SmsSDK

from celery_tasks.main import celery_app
from celery_tasks.sms import constants


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


# 使用装饰器装饰异步任务，保证celery识别任务
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    """
    发送短信验证码的异步任务
    :param mobile: 手机号
    :param sms_code: 验证码
    :return: 成功：0 失败：-1
    """
    send_ret = CCP().send_template(constants.SEND_SMS_TEMPLATE_ID, mobile,
                                   [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60])
    return send_ret
