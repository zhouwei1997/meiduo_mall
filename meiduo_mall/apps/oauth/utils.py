# -*- coding:utf-8 -*-
"""
# @author ZhouWei
# @date  2023/4/12
# @file  utils.py
# @description
"""
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData

from oauth import constants


def generate_access_token(openid):
    """
    序列化 openid
    :param openid: openid明文
    :return: token(openid密文)
    """
    # 创建序列化对象
    s = Serializer(settings.SECRET_KEY, constants.ACCESS_TOKEN_EXPIRES)
    # 准备待序列化的字典数据
    data = {'openid': openid}
    # 调用dumps方法进行序列化:type(bytes)
    token = s.dumps(data)
    # 返回序列化后的数据
    return token.decode()


def check_access_token(access_token_openid):
    """
    反解，反序列化access_token_openid
    :param access_token_openid:
    :return:
    """
    s = Serializer(settings.SECRET_KEY, constants.ACCESS_TOKEN_EXPIRES)
    # 反序列化openid密文
    try:
        data = s.loads(access_token_openid)
    except BadData:
        return None
    else:
        return data.get('openid')
